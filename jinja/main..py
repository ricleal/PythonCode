import jinja2

d = {
    "jinja_string": """CREATE OR REPLACE TABLE `{{ params.integration_dataset_name }}.users_last_assignment`
AS
with user_events_raw AS (
    SELECT
        JSON_EXTRACT_SCALAR(DATA, '$.raw_event.json_data.id') AS ms_user_id,
        DATETIME(CAST(JSON_EXTRACT_SCALAR(DATA, '$.event_fetch_time') AS TIMESTAMP)) AS event_fetched_datetime,
        JSON_EXTRACT_SCALAR(DATA, '$.organization_id') AS organization_id,
        JSON_EXTRACT_SCALAR(DATA, '$.system_id') AS system_id,
        JSON_EXTRACT_SCALAR(DATA, '$.raw_event.json_data.user_principal_name') AS principal_ms_email,
        JSON_EXTRACT_SCALAR(DATA, '$.raw_event.json_data.mail') AS principal_email,
        JSON_EXTRACT_SCALAR(DATA, '$.raw_event.json_data.display_name') AS principal_name,
        JSON_EXTRACT_ARRAY(DATA, "$.raw_event.json_data.assigned_licenses") AS assigned_licenses,
        JSON_EXTRACT_ARRAY(DATA, "$.raw_event.json_data.assigned_plans") AS assigned_plans
    FROM
        `{{ params.events_dataset_name }}.{{ params.events_table_name }}`
    WHERE
        JSON_EXTRACT_SCALAR(DATA, '$.labels.api') = 'microsoft.users'
        AND ARRAY_LENGTH(JSON_EXTRACT_ARRAY(DATA, '$.raw_event.json_data.assigned_licenses')) > 0
{% if 'organization_id' in params and params.organization_id != '' and 'system_id' in params and params.system_id != '' %}
        AND JSON_EXTRACT_SCALAR(DATA, '$.organization_id') = '{{ params.organization_id }}'
        AND JSON_EXTRACT_SCALAR(DATA, '$.system_id') = '{{ params.system_id }}'
{% endif %}
{% if 'days' in params and params.days != '' %}
        AND DATETIME_DIFF(CURRENT_DATETIME(), DATETIME(publish_time), DAY) <= {{ params.days }}
        AND DATE_DIFF(CURRENT_DATE(), DATE(_PARTITIONTIME), DAY) <= {{ params.days }}
{% else %}
        AND DATE_DIFF(CURRENT_DATE(), DATE(_PARTITIONTIME), DAY) <= 90
{% endif %}
),
""",
    "env_vars": {
        "integration_dataset_name": "integration",
        "events_dataset_name": "events",
        "events_table_name": "events",
    },
    "input": {"organization_id": "123", "system_id": "456", "days": "90"},
}

params = d.get("input", {}) | d.get("env_vars", {})


environment = jinja2.Environment()
template = environment.from_string(d["jinja_string"])
s = template.render(params=params)

print(s)
