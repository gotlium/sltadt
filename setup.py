import os
from setuptools import setup
from sltadt import VERSION

f = open(os.path.join(os.path.dirname(__file__), 'README'))
readme = f.read()
f.close()

setup(
	name='sltadt',
	version=".".join(map(str, VERSION)),
	description='Sniff your local traffic and download them by ext.',
	long_description=readme,
	author="GoTLiuM InSPiRIT",
	author_email='gotlium@gmail.com',
	url='http://github.com/gotlium/sltadt',
	packages=['sltadt'],
	include_package_data=True,
	install_requires=['setuptools', 'grab'],
	entry_points={
		'console_scripts':
			['sltadt = sltadt:run', 'wget_in_bg = sltadt.wget_in_bg:wget']
	},
	zip_safe=False,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		],
)