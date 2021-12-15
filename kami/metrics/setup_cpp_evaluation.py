from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
 

extensions = [
    Extension(language="c++", name="evaluation", sources=["evaluation.py"]),
    Extension(language="c++", name="_base_metrics", sources=["_base_metrics.py"])
]
 
setup(
    name="evaluation",
    cmdclass = {'build_ext':build_ext},
    ext_modules = cythonize(extensions),
)

