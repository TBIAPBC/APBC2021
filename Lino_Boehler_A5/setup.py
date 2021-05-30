from setuptools import setup, find_packages

setup(
   name='Lino_Boehler_A5',
   version='0.1.0',
   author='Lino Boehler',
   author_email='lino.boehler@gmx.net',
   #packages=["A0","A1","A2","A3","A4"],
   #scripts=['bin/script1','bin/script2'],
   license="MIT-License",
	 packages=find_packages(),
   description='First Package include all Exercises so far',
   long_description=open('README.txt').read(),
   install_requires=[
       "numpy"    
       
   ],
 		
)

