from setuptools import setup, find_packages
import py2exe  # For Windows executable creation

setup(
    name='LiveTranslationCaption',
    version='1.0.0',
    author='weiwang115',
    author_email='your_email@example.com',
    description='A Windows application that listens to system audio and translates Japanese language to English captions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyQt5>=5.15.10',
        'pyaudio>=0.2.13',
        'SpeechRecognition>=3.10.1',
        'googletrans==4.0.0rc1',
        'numpy>=1.24.3',
    ],
    entry_points={
        'console_scripts': [
            'live-translation-caption=main:main',
        ],
    },
    # Configuration for py2exe (Windows executable)
    windows=[{
        'script': 'src/main.py',
        'icon_resources': [(1, 'resources/icon.ico')],
        'dest_base': 'LiveTranslationCaption'
    }],
    options={
        'py2exe': {
            'bundle_files': 1,
            'compressed': True,
            'optimize': 2,
            'includes': ['PyQt5', 'speech_recognition', 'googletrans'],
        }
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
    ],
    python_requires='>=3.8',
)