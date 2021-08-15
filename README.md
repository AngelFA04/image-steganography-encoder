# Steganography encoder

Script that encode a string message into a picture using a key that is a representation 
of a color in the format of RGB. 

To use this script it is necessary to install pillow and numpy. You can do that running this command.
```
pip install -r requirements.txt
```

Examples:
```
# Encode a message in a picture
# Where 254254243 is the RGB Key
python main.py 254254243 image_without_message.jpg --encode "This is the message to encode"

# Decode a message from a picture named `encoded_image_name.png`
python main.py 254254243 encoded_image_name.png --decode

```

## NOTES:
- Right now there are many collisions of characters, it will be fixed in the future.
