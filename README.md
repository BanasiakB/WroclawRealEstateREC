# WroclawRealEstateREC
## Scrapping data
In order to start scrapping data run *main.py* file from within project root. Data will be stored in the *Data* directory and by default, the webpages that have been scrapped once, will be skipped. Scrapped data should be uploaded to the shared Google Drive, which should be the source of true for later collaboration. Please note that uploading files to Google Drive takes some time because of large number of files.

## Starting local spark environment
Spark is configured using docker containers and the architecture is described in *docker-compose.yml*. It also uses the environment variables stored in *.env* file (based on the *.env.example* schema).

### Running spark architecture for the first time
1. You need to have docker installed (enable cpu virtualisation in bios, run `wsl --install` in powershell, install *docker desktop for windows* and that should be all).
2. You should have data downloaded from the Google Drive and pasted in *Data* directory (not necessarily, but this dir will be copied to the docker container in read only mode once the container is up, so that you can work with the data there).
3. Open project root in terminal and run `docker-compose up` - that starts all the configured containers. First run will be longer since the images need to be pulled, every next run will be much shorter.
4. Now you need to connect to the jupyter container. There are 2 ways to do that:
   1. You can do nothing and search for the url with the jupyter server (starting with `127.0.0.1` and ending with a random token)
   2. You can create *.env* file based on the *.env.example* and set custom token value as `JUPYTER_TOKEN` variable. Then the url to the jupyter server will be `http://127.0.0.1:8888/lab?token={JUPYTER_TOKEN}`.
5. In the container there is a directory *pyspark_tools* which contains the same content as *pyspark_tools* dir in the project. This is the only directory within the container that will preserve after stopping the container. All its content is saved on the host machine.
6. You can connect to the container *spark-jupyter* from within Visual Studio Code in order to code form there. It is accessable from blue button on left-bottom of the IDE. You need to chose "attach to the running container"

### Running spark architecture 2nd and every next time
Steps 3-6 from above apply



