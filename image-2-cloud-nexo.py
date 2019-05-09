from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings 
import picamera

camera = picamera.PiCamera() 
camera.capture('image.jpg') 
block_blob_service = BlockBlobService(account_name='neptunstorage', account_key='8C7SDQO/19LMvAdghWtk+LC59IHEYym9QV50oGfgU+z1OoMysqqkkzIto6yNOESElFTylF8Fdk9hKVECiChALg==') 
block_blob_service.create_blob_from_path( 
   'images', 
   'nexo.jpg', 
   'image.jpg', 
   content_settings=ContentSettings(content_type='image/jpeg'))