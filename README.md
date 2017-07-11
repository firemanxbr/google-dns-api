# Google Cloud Platform DNS Tool 
This is an open source tool to management domains in Google Cloud DNS using JSON files as reference.

You can use the Jenkins or other CI for automate this task!

Benetifs about this tool:
+ All domains are versioned in Git repositories
+ All domains are based in JSON files
+ Create new zones and records

This tool was created using **Python >= 3.6**

## How-to use in 5 steps

1. Configure the project of GCP

    `$ gcloud config set project GCP_PROJECT_ID`

2. Save your credentials

    `$ gcloud auth application-default login` 

3. Install the requirements

    `$ pip3 install -r requirements.txt`

4. Create your domain using this structure into a json file, for example:
```
{
    "zone": "dns-name-of-your-zone.com.",
    "name": "name-of-your-zone-in-google-dns",
    "description": "reference about this zone, documentation purpose",
    "records": [
        {
            "name": "dns-name-of-your-zone.com.",
            "type": "A",
            "ttl": 3600,
            "value": ["8.8.8.8",
                    "8.8.4.4"]
        },
        {
            "name": "google.dns-name-of-your-zone.com.",
            "type": "CNAME",
            "ttl": 3600,
            "value": ["google.com."]
        }
    ]
}
```

5. Run the tool

    `$ python3 dns_tool.py -f my-domain-file.json`


## Reference

[Google Cloud DNS](https://cloud.google.com/dns/)
