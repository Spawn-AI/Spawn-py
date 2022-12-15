import asyncio
from postgrest import SyncPostgrestClient
from postgrest.constants import DEFAULT_POSTGREST_CLIENT_TIMEOUT

SUPABASE_URL = "https://lgwrsefyncubvpholtmh.supabase.co";
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxnd3JzZWZ5bmN1YnZwaG9sdG1oIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk0MDE0MzYsImV4cCI6MTk4NDk3NzQzNn0.o-QO3JKyJ5E-XzWRPC9WdWHY8WjzEFRRnDRSflLzHsc";

class SelasClient:
    def __init__(self, app_id, key, secret, worker_filter = { "branch" : "main" } ):
        postgrest_url = SUPABASE_URL
        postgrest_key = SUPABASE_KEY
        my_headers = {
                    "apiKey": postgrest_key,
                    "Authorization": f"Bearer {postgrest_key}",
                };
        self.client = SyncPostgrestClient(f"{postgrest_url}/rest/v1", headers=my_headers)
        self.client.auth(token=postgrest_key)
        
        self.app_id = app_id
        self.key = key
        self.secret = secret

        self.worker_filter = worker_filter

        self.services = self.getServiceList()

    def rpc(self, fn_name, params = {}):
        params["p_app_id"] = self.app_id
        params["p_key"] = self.key
        params["p_secret"] = self.secret
        return self.client.rpc(fn_name, params).execute()

    def echo(self, message):
        return self.rpc("app_owner_echo", {"message_app_owner": message})

    def getAppSuperUser(self):
        return self.rpc("app_owner_get_super_user")

    def createAppUser(self):
        return self.rpc("app_owner_create_user")

    def createToken(self, app_user_id):
        return self.rpc("app_owner_create_user_token", {"p_app_user_id": app_user_id})

    def getAppUserToken(self, app_user_id):
        return self.rpc("app_owner_get_user_token_value", {"p_app_user_id": app_user_id})

    def setCredit(self, app_user_id, amount):
        return self.rpc("app_owner_set_user_credits", {"p_app_user_id": app_user_id, "p_amount": amount})

    def getAppUserCredits(self, app_user_id):
        return self.rpc("app_owner_get_user_credits", {"p_app_user_id": app_user_id})

    def deactivateAppUser(self, app_user_id):
        return self.rpc("app_owner_deactivate_user", {"p_app_user_id": app_user_id})

    def getServiceList(self):
        return self.rpc("app_owner_get_services")

    def getServiceConfigCost(self, service_name, job_config):
        service_id = [a for a in self.services.data if a['name'] == service_name][0]['id']
        return self.client.rpc("get_service_config_cost", {"p_service_id": service_id, 
                                                        "p_config": job_config}).execute()

    def postJob(self, service_name, job_config):
        service_id = [a for a in self.services.data if a['name'] == service_name][0]['id']
        return self.rpc("app_owner_post_job_admin", {"p_service_id": service_id, 
                                                     "p_job_config": job_config,
                                                     "p_worker_filter": self.worker_filter})

    def getAppUserJobHistory(self, app_user_id, limit, offset):
        return self.rpc("app_owner_get_job_history_detail", {"p_app_user_id": app_user_id, 
                                                        "p_limit": limit, 
                                                        "p_offset": offset})

#   /**
#    * Wait for the  the result of a job and returns it.
#    * @param job_id - the id of the job.
#    * @callback - the function that will be used to process the result of the job.
#    * @example
#    *  client.subscribeToJob({job_id: response.data, callback: function (data) { console.log(data); }});
#    */
#   subscribeToJob = async (args: { job_id: string; callback: (result: object) => void }) => {
#     const client = new Pusher("ed00ed3037c02a5fd912", {
#       cluster: "eu",
#     });

#     const channel = client.subscribe(`job-${args.job_id}`);
#     channel.bind("result", args.callback);
#   };    