import requests  
import json  
  
url =  "https://imagepipeline.io/sdxl/text2image/v1/run"  
  
payload = json.dumps({  
"model_id":  "sdxl",  
"prompt":  "ultra realistic close up portrait ((beautiful pale cyberpunk female with heavy black eyeliner)), blue eyes, shaved side haircut, hyper detail, cinematic lighting, magic neon, dark red city, Canon EOS R3, nikon, f/1.4, ISO 200, 1/160s, 8K, RAW, unedited, symmetrical balance, in-frame, 8K",  
"negative_prompt":  "painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, anime",  
"width":  "512",  
"height":  "512",  
"samples":  "1",  
"num_inference_steps":  "30",  
"safety_checker":  "false",   
"guidance_scale":  7.5,  
"multi_lingual":  "no",  
"embeddings":  "", 
"lora_models": "79b34399-7159-4ae0-a5fb-1105c56bf964", 
"lora_weights":  "0.5" 
})  
  
headers =  {  
'Content-Type':  'application/json',
'API-Key': 'your_api_key'
}  
  
response = requests.request("POST", url, headers=headers, data=payload)  
  
print(response.text)


