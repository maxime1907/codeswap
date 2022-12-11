# Codeswap
Codeswap is a python application that allows for the conversion of programming languages on-the-fly using the power of natural language processing. With codeswap, you can type out code in one language and have it automatically converted to another language of your choice.

## How it Works
Codeswap uses a large language model called ChatGPT to process and understand the code that you provide. It then uses this understanding to generate equivalent code in the target language.

## Getting Started
To use codeswap, you will need to have python installed on your computer. You can check if you have python installed by running the following command in your terminal:

``` bash
python --version
```
If python is not installed, you can download and install it from the official python website.

Once you have python installed, you can clone the codeswap repository from github and install the required dependencies by running the following commands:

``` bash
git clone https://github.com/maxime1907/codeswap.git
cd codeswap
pip install -e .
```

Create a `config.yml` file that contains your credentials to authenticate with ChatGPT:
```yaml
chatgpt:
  email: "<YOUR_EMAIL>"
  password: "<YOUR_PASSWORD>"
  session_token: "<YOUR_SESSION_TOKEN>"
  proxy: "<YOUR_PROXY>"
```
More information can be found about [these parameters here](https://github.com/acheong08/ChatGPT/wiki/Setup)

With the dependencies installed, you can start using codeswap by running the following command:

``` bash
codeswap --help
```
This will start the codeswap application and allow you to input code in one language and have it converted to another language.

## Contributing
If you would like to contribute to codeswap, please fork the repository and submit a pull request with your changes. All contributions are welcome!