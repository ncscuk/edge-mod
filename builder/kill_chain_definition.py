
KILL_CHAIN_ID = "stix:TTP-af3e707f-2fb9-49e5-8c37-14026ca0a5ff"
KILL_CHAIN_NAME = "LM Cyber Kill Chain"
KILL_CHAIN_DEFINER = "LMCO"
KILL_CHAIN_PHASES = [
    {
        "phase_id": "stix:TTP-af1016d6-a744-4ed7-ac91-00fe2272185a",
        "name": "Reconnaissance",
        "ordinality": "1"
    },
    {
        "phase_id": "stix:TTP-445b4827-3cca-42bd-8421-f2e947133c16",
        "name": "Weaponization",
        "ordinality": "2"
    },
    {
        "phase_id": "stix:TTP-79a0e041-9d5f-49bb-ada4-8322622b162d",
        "name": "Delivery",
        "ordinality": "3"
    },
    {
        "phase_id": "stix:TTP-f706e4e7-53d8-44ef-967f-81535c9db7d0",
        "name": "Exploitation",
        "ordinality": "4"
    },
    {
        "phase_id": "stix:TTP-e1e4e3f7-be3b-4b39-b80a-a593cfd99a4f",
        "name": "Installation",
        "ordinality": "5"
    },
    {
        "phase_id": "stix:TTP-d6dc32b9-2538-4951-8733-3cb9ef1daae2",
        "name": "Command and Control",
        "ordinality": "6"
    },
    {
        "phase_id": "stix:TTP-786ca8f9-2d9a-4213-b38e-399af4a2e5d6",
        "name": "Actions on Objectives",
        "ordinality": "7"
    },
]
