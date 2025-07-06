import requests


def fetch_powerflow_data():
    try:
        r = requests.get("http://127.0.0.1:8888/powernetwork/powerflow/", headers={
            "Authorization": "Token e922253da7acf4a4ce14a05b7e9e24122f0718cf"
        })
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"获取潮流数据失败: {e}")
        return {'voltages': [], 'loading': []}


def fetch_topology_data():
    try:
        response = requests.get('http://127.0.0.1:8888/powernetwork/topology/', headers={
            "Authorization": "Token e922253da7acf4a4ce14a05b7e9e24122f0718cf"
        })
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching topology data: {e}")
    return {"nodes": [], "edges": []}
