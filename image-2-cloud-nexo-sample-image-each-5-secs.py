from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings 
import picamera
import time
from datetime import datetime

camera = picamera.PiCamera() 
block_blob_service = BlockBlobService(account_name='neptunstorage', account_key='8C7SDQO/19LMvAdghWtk+LC59IHEYym9QV50oGfgU+z1OoMysqqkkzIto6yNOESElFTylF8Fdk9hKVECiChALg==') 


while True:
   now = datetime.now().strftime("%d%m%Y-%H%M%S")
   camera.capture('image.jpg') 
   block_blob_service.create_blob_from_path( 
   'images', 
   'nexo-{}.jpg'.format(now), 
   'image.jpg', 
   content_settings=ContentSettings(content_type='image/jpeg'))
   time.sleep(5)
   