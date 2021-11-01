skaffold run
robusta playbooks configure c:\Users\asafh\projects\robusta\robusta\helm\asaf-active-playbook.yaml --namespace=default
robusta playbooks trigger prometheus_alert alert_name=CPUThrottlingHigh pod_name=loki-promtail-p2s8f namespace=default --namespace=default generator_url="http://prometheus-k8s-0:9090/graph?g0.expr=sum%28namespace_cpu%3Akube_pod_container_resource_requests%3Asum%29+%2F+sum%28kube_node_status_allocatable%7Bresource%3D%22cpu%22%7D%29+%3E+%28%28count%28kube_node_status_allocatable%7Bresource%3D%22cpu%22%7D%29+%3E+1%29+-+1%29+%2F+count%28kube_node_status_allocatable%7Bresource%3D%22cpu%22%7D%29&g0.tab=1"

rem kubectl logs robusta-runner-54bd797d55-ccxts -c runner -f