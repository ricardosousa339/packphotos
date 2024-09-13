import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from fast_zero.app import app


@app.get('/')
def root():
    a = 'a'
    b = 'b' + a
    return {'hello world': b}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
