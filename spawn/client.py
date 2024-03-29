from postgrest import SyncPostgrestClient
from .bind_to_events import bind_to_events
import asyncio

SUPABASE_URL = "https://lgwrsefyncubvpholtmh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxnd3JzZWZ5bmN1YnZwaG9sdG1oIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk0MDE0MzYsImV4cCI6MTk4NDk3NzQzNn0.o-QO3JKyJ5E-XzWRPC9WdWHY8WjzEFRRnDRSflLzHsc"

class SpawnClient:
    def __init__(self, app_id, key, secret, external_id = None, worker_filter={"branch": "prod"}):
        postgrest_url = SUPABASE_URL
        postgrest_key = SUPABASE_KEY
        my_headers = {
            "apiKey": postgrest_key,
            "Authorization": f"Bearer {postgrest_key}",
        }
        self.client = SyncPostgrestClient(f"{postgrest_url}/rest/v1", headers=my_headers)
        self.client.auth(token=postgrest_key)

        self.app_id = app_id
        self.key = key
        self.secret = secret

        self.app_user_id = None
        self.app_user_token = None

        self.owner_mode = True

        if external_id is not None:
            app_user_id = self.owner_rpc("app_owner_get_user_id", {"p_app_user_external_id": external_id})
            self.app_user_id = app_user_id
            self.app_user_token = self.getAppUserToken(external_id).data
            self.owner_mode = False
        self.worker_filter = worker_filter



        self.services = self.getServiceList().data
        self.addOns = self.getAddOnList().data

    def handle_error(self, error):
        if error.code == "":
            raise Exception("The database cannot be reached. Contact the administrator.)")
        if error.message == "Invalid API key":
            raise Exception("Invalid API key. Contact the administrator.")
        if error.code == "22P02":
            raise Exception("The credentials are not correct. Contact the administrator.")
        if error.code == "P0001":
            raise Exception(error.message)
        if error.code == "23505":
            raise Exception("This object already exists.")
        raise Exception("An unexpected error occured. Contact the administrator. " + error.message);
    def owner_rpc(self, fn_name, params={}):
        params["p_app_id"] = self.app_id
        params["p_key"] = self.key
        params["p_secret"] = self.secret
        try:
            return self.client.rpc(fn_name, params).execute()
        except Exception as e:
            self.handle_error(e)
        
    
    def user_rpc(self, fn_name, params={}):
        params["p_app_id"] = self.app_id
        params["p_key"] = self.key
        params["p_app_user_id"] = self.app_user_id.data
        params["p_app_user_token"] = self.app_user_token
        try:
            return self.client.rpc(fn_name, params).execute()
        except Exception as e:
            self.handle_error(e)

    def echo(self, message):
        return self.owner_rpc("app_owner_echo", {"message_app_owner": message})

    def getServiceList(self):
        if self.owner_mode:
            return self.owner_rpc("app_owner_get_services")
        else:
            return self.user_rpc("app_user_get_services")

    def getAddOnList(self):
        if self.owner_mode:
            return self.owner_rpc("app_owner_get_add_ons")
        else:
            return self.user_rpc("app_user_get_add_ons")

    # App user management

    def createAppUser(self, external_id):
        return self.owner_rpc("app_owner_create_user", {"p_external_id": external_id})

    def __getUserId(self, external_id):
        return self.owner_rpc("app_owner_get_user_id", {"p_app_user_external_id": external_id})

    def isUser(self, external_id):
        app_user_id = self.__getUserId(external_id)
        return self.owner_rpc("app_owner_is_user", {"p_app_user_id": app_user_id.data})

    def createToken(self, external_id):
        app_user_id = self.__getUserId(external_id)
        return self.owner_rpc("app_owner_create_user_token", {"p_app_user_id": app_user_id.data})

    def deleteTokenOfAppUser(self, external_id):
        app_user_id = self.__getUserId(external_id)
        token = self.owner_rpc("app_owner_get_token", {"p_app_user_id": app_user_id.data})
        return self.owner_rpc("app_owner_revoke_user_token", {"p_app_user_id": app_user_id.data, "p_token": token.data})

    def getAppUserToken(self, external_id):
        app_user_id = self.__getUserId(external_id)
        return self.owner_rpc("app_owner_get_user_token_value", {"p_app_user_id": app_user_id.data})

    def setCredit(self, external_id, amount):
        app_user_id = self.__getUserId(external_id)
        return self.owner_rpc(
            "app_owner_set_user_credits", {"p_app_user_id": app_user_id.data, "p_amount": amount}
        )

    def getAppUserCredits(self, external_id):
        app_user_id = self.__getUserId(external_id)
        return self.owner_rpc("app_owner_get_user_credits", {"p_app_user_id": app_user_id.data})

    def getAppUserJobHistory(self, external_id, limit, offset):
        app_user_id = self.__getUserId(external_id)
        return self.owner_rpc("app_owner_get_job_history_detail",
                        {"p_app_user_id": app_user_id.data, "p_limit": limit, "p_offset": offset},
    )

    # Add on management
    def renameAddOn(self, add_on_name, new_name):
        add_on = [a for a in self.addOns if a["name"] == add_on_name][0]
        return self.owner_rpc("app_owner_rename_add_on", {"p_add_on_id": add_on["id"], "p_new_name": new_name})

    def shareAddOn(self, add_on_name, external_id):
        add_on = [a for a in self.addOns if a["name"] == add_on_name][0]
        return self.owner_rpc("app_owner_share_add_on", 
                {"p_add_on_id": add_on["id"], "p_app_user_external_id": external_id})

    def deleteAddOn(self, add_on_name):
        add_on = [a for a in self.addOns if a["name"] == add_on_name][0]
        return self.owner_rpc("app_owner_delete_add_on", {"p_add_on_id": add_on["id"]})

    def publishAddOn(self, add_on_name):
        add_on = [a for a in self.addOns if a["name"] == add_on_name][0]
        return self.owner_rpc("app_owner_publish_add_on", {"p_add_on_id": add_on["id"]})

    def unpublishAddOn(self, add_on_name):
        add_on = [a for a in self.addOns if a["name"] == add_on_name][0]
        return self.owner_rpc("app_owner_unpublish_add_on", {"p_add_on_id": add_on["id"]})
        
    # post job
    def getCountActiveWorker(self):
        return self.owner_rpc("get_active_worker_count", 
                {"p_worker_filter": self.worker_filter})

    def postJob(self, service_name, job_config):
        service = [a for a in self.services if a["name"] == service_name][0]
        if self.owner_mode:
            return self.owner_rpc(
                "app_owner_post_job_admin",
                {
                    "p_service_id": service['id'],
                    "p_job_config": job_config,
                    "p_worker_filter": self.worker_filter,
                },
            )
        else:
            return self.user_rpc(
                "post_job",
                {
                    "p_service_id": service['id'],
                    "p_job_config": job_config,
                    "p_worker_filter": self.worker_filter,
                },
            )

    def costPatchTrainer(self, dataset, patch_name, 
        service_name = 'patch_trainer_v1', 
        description = '', 
        learning_rate = 1e-4, 
        steps = 100, 
        rank = 4):
        service = [a for a in self.services if a["name"] == service_name][0]
        job_config = {
            "dataset": dataset,
            "patch_name": patch_name,
            "description": description,
            "learning_rate": learning_rate,
            "steps": steps,
            "rank": rank,
        }
        return self.client.owner_rpc(
            "get_service_config_cost_client",
            {
                "p_service_id": service['id'],
                "p_config": job_config,
            }
        ).execute()

    def runPatchTrainer(self, dataset, patch_name, 
        service_name = 'patch_trainer_v1', 
        description = '', 
        learning_rate = 1e-4, 
        steps = 100, 
        rank = 4,
        callback = print):
        job_config = {
            "dataset": dataset,
            "patch_name": patch_name,
            "description": description,
            "learning_rate": learning_rate,
            "steps": steps,
            "rank": rank,
        }
        job =  self.postJob(service_name, job_config)
        self.subscribeToJob(job.data['job_id'],callback)
        return job

    def __patchConfigToAddonConfig(self, patch_config):
        patch_id = [a for a in self.addOns if a["name"] == patch_config["name"]][0]['id']
        return {
            "id": patch_id,
            "config" : {
                "alpha_unet": patch_config["alpha_unet"],
                "alpha_text_encoder": patch_config["alpha_text_encoder"],
                "steps": patch_config["steps"],
            }
        }

    def costStableDiffusion(self, prompt,
      service_name = "stable-diffusion-2-1-base",
      steps = 28,
      skip_steps = 0,
      batch_size = 1,
      sampler = "k_euler",
      guidance_scale = 10,
      width = 512,
      height = 512,
      negative_prompt = 'ugly',
      image_format = "jpeg",
      translate_prompt = False,
      nsfw_filter = False,
      patches = []):
        service = [a for a in self.services if a["name"] == service_name][0]

        add_ons = [self.__patchConfigToAddonConfig(patch) for patch in patches]

        job_config = {
            "steps": steps,
            "skip_steps": skip_steps,
            "batch_size": batch_size,
            "sampler": sampler,
            "guidance_scale": guidance_scale,
            "width": width,
            "height": height,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "image_format": image_format,
            "translate_prompt": translate_prompt,
            "nsfw_filter": nsfw_filter,
            "add_ons": add_ons,
        };

        return self.client.owner_rpc(
            "get_service_config_cost_client",
            {
                "p_service_id": service['id'],
                "p_config": job_config,
            }
        ).execute()

    def runStableDiffusion(self, prompt,
      service_name = "stable-diffusion-2-1-base",
      steps = 28,
      skip_steps = 0,
      batch_size = 1,
      sampler = "k_euler",
      guidance_scale = 10,
      width = 512,
      height = 512,
      negative_prompt = 'ugly',
      image_format = "jpeg",
      translate_prompt = False,
      nsfw_filter = False,
      patches = [],
      callback = print):

        add_ons = [self.__patchConfigToAddonConfig(patch) for patch in patches]

        job_config = {
            "steps": steps,
            "skip_steps": skip_steps,
            "batch_size": batch_size,
            "sampler": sampler,
            "guidance_scale": guidance_scale,
            "width": width,
            "height": height,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "image_format": image_format,
            "translate_prompt": translate_prompt,
            "nsfw_filter": nsfw_filter,
            "add_ons": add_ons,
        };
        job =  self.postJob(service_name, job_config)
        self.subscribeToJob(job.data['job_id'],callback)
        return job

    # Results
    def getResults(self, job_id):
        return self.owner_rpc("app_owner_get_result", {"p_job_id": job_id})

    def subscribeToJob(self, job_id, callbacks):
        asyncio.run(bind_to_events(job_id,callbacks))


