# Ziri-inLLAMA
This is a project to deploy 'llama.cpp' with the email, especially on some small devices, such as Raspberry Pi or Orange Pi. Let the email learn to speak.  
  
## Quick Start
1. Download or clone the repository -- [`llama.cpp`](https://github.com/ggerganov/llama.cpp) and unzip it to the current directory.  
   After completing these steps, your directory structure may will look like this:
   ```
   __init__.py
   llama.cpp-master
   mail
   main_direct.py
   main.py
   ```
2. Install Python dependencies.
   ```
   numpy
   sentencepiece
   ```
4. Switch to the compilation path and compile it.
   ```
   cd llama.cpp
   make
   ```
5. Place model weights in the `./llama.cpp-master/models/` folder.  
   e.g. It may be like: `.../llama.cpp-master/models/7B/ggml-model-q4_1.bin`
7. Adjusting the email parameters in [`./mail/mail_options.py`](./mail/mail_options.py).
8. Run [`main.py`](./main.py)

## Some other statements
- In principle, the LLaMA models are officially distributed by Facebook and should not be provided through this repository. So please refer to [Facebook's LLaMA repository](https://github.com/facebookresearch/llama) if you need to request access to the model data.
