"""High Level Interface for `OpenGL Shaders <http://www.opengl.org/wiki/Shader>`_"""
#(C) Fabian Dill 2009-2014


from OpenGL.GL import *
from ctypes import c_char_p, cast, byref, c_char, create_string_buffer, POINTER
from shaderlib import *
import random


__docformat__ = 'restructuredtext'
__all__ = {"Shader", "DerpShader", "Program", "DerpProgram", "init"}

class Shader():
    
    """A single Shader to make a Program
    
    Example::
    
        vertex = Shader(open("my_shader.txt","b").read())
        Program([vertex])"""
    
    def __init__(self, source,stype = None, prefix = b"#version 330 compatibility\n#define GL_ARB_shading_language_420pack    1\n"):
        """Create a Shader from source code
        
        **Arguments**:
            `source` : bytes
                Shader Source Code.
            `stype` : int
                OpenGL Constant to identify Shader Type, not needed if source code starts with //<name of shadertype> .
            `prefix` : bytes
                Text that is inserted before shader source, for defines, version and languagepack specifications.
        """

        self.prefix = prefix
        self.typebind = {}
        foundtype, self.source = self.search(source)
        if stype == None:
            stype = foundtype
        self.id = glCreateShader(stype)
        if self.source:self._compile()
        
    def __del__(self):
        glDeleteShader(self.id)
        
    def search(self, source):
        """search Shader source code for shader type, imports and uniforms.
        
        Uniforms are saved in Shader.typebind
        Shader Type is returned
        Imports are applied and modified source is returned
        
        **Arguments**:
            `source` : bytes
                Shader Source Code.

        **returns**:
            (int, bytes) : Shader Type OpenGL Constant and modified source
        """
        stype = None
        prefix = self.prefix
        split = source.split()
        for i,s in enumerate(split):
            if s.startswith(b"//"):
                if s[2:] == b"fragment":
                    stype = GL_FRAGMENT_SHADER
                    self.type = "Fragment"
                elif s[2:] == b"vertex":
                    stype = GL_VERTEX_SHADER
                    self.type = "Vertex"
                elif s[2:] == b"geometry":
                    stype = GL_GEOMETRY_SHADER
                    self.type = "Geometry"
                elif s[2:].startswith(b"import"):
                    prefix += globals()[s[9:].decode()]

            if s == b"uniform":
                vartype = split[i+1]
                varname = split[i+2].strip(b";")
                found = True
                
                if vartype == b"float":
                    vartype = glUniform1f
                elif vartype == b"vec2":
                    vartype = glUniform2f
                elif vartype == b"vec3":
                    vartype = glUniform3f
                elif vartype == b"vec4":
                    vartype = glUniform4f  
                elif vartype == b"int":
                    vartype = glUniform1i
                elif vartype == b"ivec2":
                    vartype = glUniform2i
                elif vartype == b"ivec3":
                    vartype = glUniform3i
                elif vartype == b"ivec4":
                    vartype = glUniform4i  
                elif vartype.startswith(b"sampler"):
                    vartype = b"sampler"

                else: 
                    print(("Warning; unknown uniform variable %s" % vartype))
                    found = False
                if found:
                    if varname.endswith(b"]"):
                        base, count = (varname.split(b"["))
                        count = count.rstrip(b"]")
                        for x in range(int(count)):self.typebind[("%s[%d]" % (base.decode(), x)).encode()] = vartype
                    else:self.typebind[varname] = vartype
        return stype, prefix+source
        
    def _compile(self):
        """Compile the shader from source"""
        
        ptr = cast(c_char_p(self.source), POINTER(c_char))
        glShaderSource(self.id, 1, byref(ptr), None)
        glCompileShader(self.id)
        status = GLint(0)
        glGetShaderiv(self.id, GL_COMPILE_STATUS, byref(status))
        log = self.check()    
        if not status.value == GL_TRUE:
            
            print ("Error in shader. Source code:")
            dsource = self.source.decode()
            print (dsource)
            log = findlines(log, dsource)
            raise Exception(log)
        
    def check(self):
        """Check Shader for infos
        
        **returns**:
            str : Shader Info Log
        """
        length = GLint(0)
        glGetShaderiv(self.id, GL_INFO_LOG_LENGTH, byref(length))
        log = create_string_buffer(length.value)
        glGetShaderInfoLog(self.id, length.value, None, log)
        return log.value.decode()
    
def findlines(log, source):
    """Locate an error in source via error message
    
    **Arguments**:
        `log` : bytes
            Error log from OpenGL
        `source` : bytes
            Shader source code
    
    **returns**:
        str : Exception text with relevant shader source lines"""
    
    
    nsource = source.split("\n")
    nlog = log.split("\n")
    x = 0
    while x < len(nlog):
        line = nlog[x]
        if line.startswith("ERROR") or line.startswith("WARNING"):
            sline = line.split()[1]
            try:sline = int(sline.split(":")[1])
            except:pass
            else:
                text = "\n".join(nsource[max(sline-2,0): sline+1])
                nlog.insert(x, text)
                x+= 1
        x += 1
    return "\n".join(nlog)

inttypes = (glUniform1i,glUniform2i,glUniform3i,glUniform4i)

class Program():
    """Wrapper for OpenGL Shader Programs
    
    Can be used using the with statement.
    
    Example::
    
        prog = Program(shaders)
        with prog:
            render_stuff()
    """
    
    def __init__(self, shaders):
        """Create a Shader Program from Shaders.
        
        **Arguments**
            `shaders` : iterable of :class:`.Shader`.
                instances of shader.Shader Objects"""
                
        self.id = glCreateProgram()
        
        self.binding = {}
        self.typebind = {}
        self.texbind = []
        for shader in shaders:
            glAttachShader(self.id, shader.id)
            self.typebind.update(shader.typebind)

        glLinkProgram(self.id)
        for shader in shaders:
            
            glDetachShader(self.id, shader.id)
        self.bind()
        self.bound = True
        for name, func in list(self.typebind.items()):
            if func == "sampler":
                self.binding[name] = glGetUniformLocation(self.id, c_char_p(name))
                glUniform1i(self.binding[name], len(self.texbind))
                self.texbind.append(name)
            else:
                self.binding[name] = glGetUniformLocation(self.id, c_char_p(name))

        self.unbind()
        status = GLint(0)
        glGetProgramiv(self.id, GL_LINK_STATUS, byref(status))
        log = self.check()
        
        if not status.value == GL_TRUE:
            raise Exception (log)
        self.__enter__ = self.bind #direct overwrite for performance
        self.seed()

    def seed(self):
        """Create a random seed and insert into seed uniform,
        if one was created via 'uniform float seed;' in Shader source"""
        with self:
            for name in self.typebind:
                if name.startswith(b"seed"):
                    self[name] = (random.random()-0.5)*100000.0,
                    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """unbind Program when exiting with statement"""
        glUseProgram(GLuint(0))
        
    def __enter__(self):
        """bind Program when entering with statement"""
        self.bind()
    
    def __del__(self):
        glDeleteProgram(self.id)
        
    def set_texture(self, name, texture):
        """set sampler uniform"""
        if not self.bound:raise RuntimeError("Attempted to upload data to unbound Shader.")
        if name in self.texbind:
            i = self.texbind.index(name)
        else:    
            i = len(self.texbind)
            glUniform1i(self.binding[name], i)
            self.texbind.append(name)
        glActiveTexture(GL_TEXTURE0+i)
        glBindTexture(GL_TEXTURE_2D, texture)
        
    def set_array(self, arrayname, array):
        """Set an uniform array
        
        **Arguments**:
            `arrayname` : str
                name of uniform
            `array` : iterable
                data to upload
        """
        if not self.bound:raise RuntimeError("Attempted to upload data to unbound Shader.")
        key = arrayname+"[0]"
        bind = self.typebind[key]
        base = GLint if bind in inttypes else GLfloat
        for x, item in zip(list(range(self.binding[key], self.binding[key]+len(array))), array):
            bind(x, *[base(v) for v in item])
            
    def __setitem__(self, key, values):
        """set a single uniform
        Alias for Shader[key] = values
        
        **Arguments**:
            `key` : str
                name of uniform
            `values` : iterable
                Values to fill the uniform with"""

        if not self.bound:raise RuntimeError("Attempted to upload data to unbound Shader.")
        bind = self.typebind[key]
        if bind in inttypes:
            bind(self.binding[key], *[GLint(value) for value in values])
        else:
            bind(self.binding[key], *[GLfloat(value) for value in values])

    set_uniform = __setitem__
    
    def check(self):
        """check Compiler Info Log
        
        **returns**:
            str : Compiler Info Log"""
        length = GLint()
        glGetProgramiv(self.id, GL_INFO_LOG_LENGTH, byref(length))
        log = create_string_buffer(length.value)
        glGetProgramInfoLog(self.id, length.value, None, log)
        return log.value.decode()
    
    def bind(self):
        """Use the program. Called when entering via with Statement"""
        glUseProgram(self.id)
        self.bound = True
        
    def unbind(self):
        """Disable the Program. Called when exiting with statement"""
        glUseProgram(GLuint(0))
        self.bound = False
        
class DerpProgram():
    """Replacement for :class:`.Program`, that does nothing"""
    def __init__(self, *args, **kwargs):pass
    def __exit__(self, exc_type, exc_val, exc_tb):pass
    def __enter__(self):pass
    def __del__(self):pass
    def __setitem__(self, key, value):pass
    def check(self):pass
    def bind(self):pass
    def unbind(self):pass
    def seed(self):pass
    
class DerpShader():
    """Replacement for :class:`.Shader`, that does nothing"""
    def __init__(self, *args, **kwargs):pass
    def _compile(self, *args):pass
    def check(self):pass
    
def init(use_shaders):
    "Init module. If use_shaders is False, replace :class:`.Program` and :class:`.Shader` with Derps"
    import sys
    if not use_shaders and not sys.argv[0].endswith("sphinx-build-script.py"):
        globals()["Program"] = DerpProgram
        globals()["Shader"] = DerpShader

class Texture1D():
    """Experimental, do not touch"""
    def __init__(self, length):
        self.id = GLuint()
        glGenTextures(1, byref(self.id))
        glBindTexture(GL_TEXTURE_1D, self.id)
        glTexImage1D(GL_TEXTURE_1D, 0, GL_ALPHA16,  length, 0, GL_RGBA8, GL_FLOAT, None)
    def assign(self, iterable):
        glBindTexture(GL_TEXTURE_1D, self.id)
        data = (GLdouble * len(iterable))()
        for i,d in enumerate(iterable):
            data[i] = d
        glTexSubImage1D(GL_TEXTURE_1D, 0,0,len(iterable)//4, GL_RGBA8, GL_FLOAT, byref(data))
    def bind_to_unit(self, unit):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_1D, self.id)
        glActiveTexture(GL_TEXTURE0)
        
