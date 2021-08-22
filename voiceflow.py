import requests

# View our quick start guide to get your API key and version ID:
# https://www.voiceflow.com/api/dialog-manager#section/Quick-Start
api_key = "VF.6121b1f2dab770001b3409b8.wiNdlgj7y6yt4pmat9hpt0ezktL899y2T0OgevHGUB"
version_id = "61216a6b47d41a00062ca40a"

def request(user_id, user_input):
    body = {"request": {"type": "text", "payload": user_input}}

    # Start a conversation
    response = requests.post(
        f"https://general-runtime.voiceflow.com/state/{version_id}/user/{user_id}/interact",
        json=body,
        headers={"Authorization": api_key},
    )

    indications = []
    options = []
    print("{} {} {}".format(user_id,user_input,response.json()))
    for i in response.json():
        if i["type"] == "speak":
            indications.append(i["payload"]["message"])
        elif i["type"] == "choice":
            options += [j["name"] for j in i["payload"]["buttons"]]
    
    # Log the response
    print('\n'.join(indications))
    print(' '.join(options))
    return {"indications": indications, "options": options}
