import json


def check_callback_btn_type(data: str | list | tuple):
    def get_json(c) -> dict:
        try:
            return json.loads(c.data)
        except json.JSONDecodeError:
            return dict()
        
    if isinstance(data, str):
        return lambda x: get_json(x).get('type') == data
    else:
        return lambda x: get_json(x).get('type') in data
    