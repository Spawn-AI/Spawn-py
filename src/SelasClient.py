import asyncio
from postgrest import SyncPostgrestClient
from postgrest.constants import DEFAULT_POSTGREST_CLIENT_TIMEOUT

SUPABASE_URL = "https://lgwrsefyncubvpholtmh.supabase.co";
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxnd3JzZWZ5bmN1YnZwaG9sdG1oIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk0MDE0MzYsImV4cCI6MTk4NDk3NzQzNn0.o-QO3JKyJ5E-XzWRPC9WdWHY8WjzEFRRnDRSflLzHsc";

class SelasClient:
    def __init__(self, app_id, key, secret ):
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

    def addCredit(self, app_user_id, amount):
        return self.rpc("app_owner_add_user_credits", {"p_app_user_id": app_user_id, "p_amount": amount})

    def getAppUserCredits(self, app_user_id):
        return self.rpc("app_owner_get_user_credits", {"p_app_user_id": app_user_id})

    def deactivateAppUser(self, app_user_id):
        return self.rpc("app_owner_deactivate_user", {"p_app_user_id": app_user_id})

    def getServiceList(self):
        return self.rpc("app_owner_get_services")

#   getAppUserJobHistoryDetail = async (args: { app_user_id: string; p_limit: number; p_offset: number }) => {
#     const { data, error } = await this.rpc("app_owner_get_job_history_detail", {
#       p_app_user_id: args.app_user_id,
#       p_limit: args.p_limit,
#       p_offset: args.p_offset
#     });
#     return { data, error };
#   };

#   /**
#    * Create a new job. This job will be executed by the workers of the app.
#    * @param service_id - the id of the service that will be executed.
#    * @param job_config - the configuration of the job.
#    * @returns the id of the job.
#    */
#   postJob = async (args: { service_id: string; job_config: string }) => {
#     const { data, error } = await this.rpc("app_owner_post_job_admin", {
#       p_service_id: args.service_id,
#       p_job_config: args.job_config,
#       p_worker_filter: this.worker_filter,
#     });
#     return { data, error };
#   };

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