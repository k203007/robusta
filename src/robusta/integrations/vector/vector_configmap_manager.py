import logging
import pkgutil
import time

import jinja2
from typing import List
from .models import OnPogLogConfig
from ...model.playbook_definition import PlaybookDefinition
from ...integrations.kubernetes.autogenerated.v1.models import ConfigMap, RobustaPod
from hikaru.model.rel_1_16 import PodList
from ...core.model.env_vars import INSTALLATION_NAMESPACE


# TODO: lets export a more general integration API here
class VectorConfigMapManager:
    def on_init(self):
        pass

    def on_playbooks_update(self, active_playbooks: List[PlaybookDefinition]):
        log_triggers = self.__get_log_triggers(active_playbooks)
        template = jinja2.Template(
            pkgutil.get_data(__package__, "vector_configmap_template.yaml").decode()
        )
        rendered_template = template.render(log_triggers=log_triggers)
        logging.info(f"updating vector config wth: {rendered_template}")

        config_map: ConfigMap = ConfigMap.readNamespacedConfigMap(
            "robusta-vector", INSTALLATION_NAMESPACE
        ).obj
        config_map.data["vector.yaml"] = rendered_template
        # TODO: sometimes this fails when the helm chart is still being rolled out and the resource is changed
        # TODO: possibly using replace instead of update would fix this, though we might mess up certain labels
        # it might be best to just have vector load an external config which we provide...
        config_map.update()

        # give nodes time to sync the configmap - this is bad as it pauses the entire runner for 5 seconds
        time.sleep(5)

        # cause robusta-vector to reload. see:
        # https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#mounted-configmaps-are-updated-automatically
        pods: PodList = PodList.listNamespacedPod(INSTALLATION_NAMESPACE).obj
        for pod in pods.items:
            if not pod.metadata.name.startswith("robusta-vector"):
                continue
            pod.metadata.annotations["lastConfigMapUpdate"] = f"{time.time()}"
            pod.update()

    @staticmethod
    def __get_log_triggers(
        active_playbooks: List[PlaybookDefinition],
    ) -> List[OnPogLogConfig]:
        log_triggers = []
        for playbook in active_playbooks:
            if len(playbook.triggers) != 1:
                raise Exception(
                    "Playbooks with more than one trigger are not supported"
                )
            trigger = playbook.triggers[0].get()
            logging.warning(f"checking trigger {trigger}, type is {type(trigger)}")
            if isinstance(trigger, OnPogLogConfig):
                logging.warning("YES")
                log_triggers.append(trigger)
        return log_triggers