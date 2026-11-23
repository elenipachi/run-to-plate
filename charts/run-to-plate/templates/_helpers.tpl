{{- define "run-to-plate.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "run-to-plate.fullname" -}}
{{- if contains (include "run-to-plate.name" .) .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name (include "run-to-plate.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "run-to-plate.selectorLabels" -}}
app.kubernetes.io/name: {{ include "run-to-plate.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "run-to-plate.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" }}
{{ include "run-to-plate.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
