#
# Copyright (C) 2015 The Regents of the University of California.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

from setuptools import setup, Extension, find_packages

_pybgpstream_module = Extension("_pybgpstream",
                                libraries = ["bgpstream"],
                                sources = ["src/_pybgpstream_module.c",
                                           "src/_pybgpstream_bgpstream.c",
                                           "src/_pybgpstream_bgprecord.c",
                                           "src/_pybgpstream_bgpelem.c"])

setup(name = "pybgpstream",
      description = "A Python interface to BGPStream",
      long_description = "Provides a high-level interface for live and historical BGP data analysis. PyBGPStream requires the libBGPStream C library, available at http://bgpstream.caida.org/download.",
      version = "2.0.0",
      author = "Alistair King",
      author_email = "bgpstream-info@caida.org",
      url="http://bgpstream.caida.org",
      license="BSD",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'Intended Audience :: System Administrators',
          'Intended Audience :: Telecommunications Industry',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX',
          ],
      keywords='_pybgpstream pybgpstream bgpstream bgp mrt routeviews route-views ris routing',
      packages=find_packages(),
      install_requires=['python-dateutil'],
      ext_modules=[_pybgpstream_module, ])
