

def import_string(import_name):
    '''
    Import class from String
    '''
    try:
        if '.' in import_name:
            module, obj = import_name.rsplit('.', 1)
            return getattr(__import__(module, None, None, [obj]), obj)
        else:
            return __import__(import_name)
    except (ImportError, AttributeError), e:
        print e

Objects = import_string('Geometry.vtk2.Objects')
o = Objects()
#o.create_cylinder()
o.create_arrow()
o.view()
