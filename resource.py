import yaml


class Resource:
    def __init__(self, name: str, resource_id: str):
        self.name = name
        self.resource_id = resource_id


class Park:
    def __init__(self, name: str, region_name: str, country_name: str, resources: list = None):
        self.name = name
        self.region_name = region_name
        self.country_name = country_name
        self.resources = resources


def _load_yaml():
    with open('resources.yaml', 'r') as file:
        data = yaml.safe_load(file)
    return data


def _get_resources(data, resources=None, concat=""):
    if resources is None:
        resources = []
    if data:
        for resource_data in data:
            name = (concat + " " + resource_data['name']).strip()
            if resource_data.get('resources'):
                resources = _get_resources(resource_data['resources'], resources, name)
            else:
                resource = Resource(
                    name=name,
                    resource_id=resource_data['resource_id']
                )
                resources.append(resource)
    return resources


def _parse_yaml_to_objects(data):
    parks = []
    for park_data in data['parks']:
        park = Park(
            name=park_data['name'],
            region_name=park_data['region_name'],
            country_name=park_data['country_name'],
            resources=_get_resources(park_data.get('resources'))
        )
        parks.append(park)
    return parks


def load_park_resources():
    data = _load_yaml()
    return _parse_yaml_to_objects(data)
