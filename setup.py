from setuptools import setup, find_packages

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Ali Mahmud',
    author_email='a.mahmud13032@gmail.com',
    install_requires=['openai','langchain','streamlit','python-dotenv','PyPDF2'],
    packages=find_packages()
)