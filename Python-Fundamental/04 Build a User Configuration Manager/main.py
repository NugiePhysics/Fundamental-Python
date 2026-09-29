'''
In this lab, you will build a User Configuration Manager that allows users to manage their settings such as theme, language, and notifications.
You will implement functions to add, update, delete, and view user settings.
'''

def add_setting(dictionary, settings):
    if isinstance(settings, (tuple, list)):
        key, value = settings
    else:
        key, value = settings, settings
    
    key = str(key).lower()
    value = str(value).lower()

    if key in dictionary:
        return f"Setting '{key}' already exists! Cannot add a new setting with this name."
    else:
        dictionary[key] = value
        return f"Setting '{key}' added with value '{value}' successfully!"

def update_setting(dictionary, settings):
    if isinstance(settings, (tuple, list)):
        key, value = settings
    else:
        key, value = settings, settings

    key = str(key).lower()
    value = str(value).lower()

    if key in dictionary:
        dictionary[key] = value
        return f"Setting '{key}' updated to '{value}' successfully!"
    else:
        return f"Setting '{key}' does not exist! Cannot update a non-existing setting."

def delete_setting(dictionary, settings):
    if isinstance(settings, (tuple, list)):
        key = settings[0]
    else:
        key = settings
    
    key = str(key).lower()

    if key in dictionary:
        dictionary.pop(key)
        return f"Setting '{key}' deleted successfully!"
    else:
        return f"Setting not found!"

def view_settings(dictionary):
    if not dictionary:
        return "No settings available."
    
    result = "Current User Settings:\n"
    for key,value in dictionary.items():
        result += f"{key.capitalize()}: {value}\n"
    return result

test_settings = {
    'theme': 'dark',
    'notifications': 'enebled',
    'volume': 'high'
}

print(delete_setting({'theme': 'light'}, 'theme'))