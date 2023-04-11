import json
import os
import subprocess

file_path = "../cicd_apps_info.json"
f = open(file_path)
data = json.load(f)
f.close()
env = "prod"

def create_new_secret(group, app, file):
  cmd = "op document create %s --title %s --vault %s-%s" % (file, app, group, env)
  print(cmd)
  process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()

  print(output, error)
  
for d in os.listdir("./" + env):
  list_files = os.listdir("./%s/%s" % (env, d))
  list_files.sort()
  app_name = d
  group_name = data[env][app_name]
  flag = 0
  for f in list_files:
    s3_file = "./%s/%s/%s" % (env, d, f)
    if os.stat(s3_file).st_size != 0 and group_name != None:
      if flag == 0:
        create_new_secret(group_name, app_name, s3_file)
        flag = 1
      else:
        create_new_secret(group_name, "%s-%s" % (app_name, os.path.splitext(os.path.basename(s3_file))[0]), s3_file)