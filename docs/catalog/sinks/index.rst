Sinks
======

Playbooks results can be sent to one or more sinks.

Supported sinks
^^^^^^^^^^^^^^^^^^^^^
Currently four sink types are supported:

* :ref:`slack`
* `Robusta UI <https://home.robusta.dev/ui/>`_ - send playbooks results to Robusta's web UI
* MS Teams - send playbooks results to an MS Teams channel webhook.
* Kafka - send playbooks results to a Kafka topic
* Datadog - send playbooks results to the Datadog events API

For sinks configuration options see :ref:`Defining additional sinks`

Formatting data for sinks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For the most part, playbooks are sink-agnostic. Data will automatically be formatted appropriately for each sink.

The output from ``resource_babysitter`` looks like this in the different sinks:

**Robusta UI:**

    .. image:: /images/deployment-babysitter-ui.png
      :width: 1000
      :align: center

**Slack:**

    .. image:: /images/deployment-babysitter-slack.png
      :width: 600
      :align: center

**MS Teams:**

    .. image:: /images/deployment-babysitter-teams.png
      :width: 600
      :align: center

**kafka:**

    .. image:: /images/deployment-babysitter-kafka.png
      :width: 400
      :align: center

**Datadog:**

    .. image:: /images/deployment-babysitter-datadog.png
      :width: 1000
      :align: center

Default sinks
-------------
If a playbook doesn't specify a sink then output will be sent to the default sinks. A sink is considered default
if it has the field `default: true` in the yaml.

Sink documentation
^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   slack
