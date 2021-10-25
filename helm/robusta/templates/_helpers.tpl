{{ define "robusta.configfile" -}}
{{- if or .Values.slackApiKey .Values.robustaApiKey }}
sinks_config:
  {{- if .Values.slackApiKey }}
  - sink_name: slack_sink
    sink_type: slack
    params:
      api_key: {{ .Values.slackApiKey }}
      slack_channel: {{ required "A valid .Values.slackChannel entry is required!" .Values.slackChannel }}
  {{- end }}
  {{- if .Values.msteamsWebhookUrl }}
  - sink_name: msteams_sink
    sink_type: msteams
    params:
      msteams_hookurl: {{ .Values.msteamsWebhookUrl }}
  {{- end }}
  {{- if .Values.robustaApiKey }}
  - sink_name: robusta_ui_sink
    sink_type: robusta
    params:
      token: {{ .Values.robustaApiKey }}
  {{- end }}
{{- end }}
global_config:
{{- if or .Values.slackApiKey .Values.robustaApiKey .Values.msteamsWebhookUrl }}
  sinks:
  {{- if .Values.slackApiKey }}
  - slack_sink
  {{- end }}
  {{- if .Values.msteamsWebhookUrl }}
  - msteams_sink
  {{- end }}
  {{- if .Values.robustaApiKey }}
  - robusta_ui_sink
  {{- end }}
{{- end }}
  cluster_name: {{ required "A valid .Values.clusterName entry is required!" .Values.clusterName }}
active_playbooks:
{{ toYaml .Values.playbooks | indent 2 }}
{{ end }}
