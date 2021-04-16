'''
这个库的安装方式很简单，直接使用 pip 就可以，我使用 Python 3 版本，安装命令如下：
pip3 install loguru
小试牛刀
安装完毕之后，我们就可以使用了，最简单的使用方式：
'''
from loguru import logger


logger.debug('this is a debug message')

'''
无需任何配置，即取即用。上例是打印一条 debug 级别的日志，输出结果如下：

2021-03-16 22:17:23.640 | DEBUG    | __main__:<module>:8 - this is a debug message

这条输出日志信息包含了日期、时间、日志级别、日志代码行数以及日志内容信息。可以说最基本的内容都囊括了，当然你还可以打印 warning、info、error、critical、success 等级别。输出的日志在 console 中还带有高亮颜色，并且每个级别的日志颜色不一样，简直不要太酷！
'''

'''
日志文件
写文件
在loguru中，输出日志文件只需要一个 add() 函数即可：
'''
logger.add('hello.log')

logger.debug('i am in log file')

'''
这时候，在 console 中会正常打印日志信息，在同级目录下会生成一个日志文件 hello.log ，我们打开日志文件，可以看到内容如下：

2021-03-16 21:20:31.460 | DEBUG    | __main__:<module>:12 - i am in log file

当然，我们还可以加一些参数，来指定文件中日志输出的格式、级别：
'''
log = logger.add('world.log', format="{time} | {level} | {message}", level="INFO")

logger.debug('i am debug message')
logger.info('i am info message')

'''
对应的文件输出信息如下：

2021-03-16T22:47:53.226998+0800 | INFO | i am info message

我们设置了文件只记录 info 级别的信息，所以 debug 级别的日志信息并没有写入日志文件。
我们也可以给日志文件名称加信息：
'''
logger.add('hello_{time}.log')

'''
上面的代码运行后，会生成一个带时间的日志文件。
停止写入文件
当我们不再需要将日志写入文件时，我们随时可以停止：
'''
id = logger.add('world.log', format="{time} | {level} | {message}", level="INFO")
logger.info('this is a info message')
logger.remove(id)
logger.info('this is another info message')

'''
add() 方法会返回一个日志文件的 id ，当我们需要停止写入信息时，我们使用 remove() 方法，传入 id ，即可。上面代码运行后，日志文件记录的信息如下：

2021-03-16T22:47:53.227389+0800 | INFO | this is a info message

在调用 remove() 方法后，其后面的日志信息并没有写入日志文件中。
滚动记录日志文件
我们可以配置 rotation 参数，来指定日志文件的生成方式，跟通常的日志记录一样，我们可以设置按照文件大小、时间、日期等来指定生成策略。
'''
# 超过200M就新生成一个文件
logger.add("size.log", rotation="200 MB")
# 每天中午12点生成一个新文件
logger.add("time.log", rotation="12:00")
# 一周生成一个新文件
logger.add("size.log", rotation="1 week")

#指定日志文件的有效期
#我们还可以通过 retention 参数来指定日志文件的保留时长：

logger.add("file.log", retention="30 days") 

#通过上面的配置，可以指定日志文件最多保留30天，30天之前的日志文件就会被清理掉。
#配置压缩文件
#为了节省空间，我们可能存在压缩日志文件的需求，这个 loguru 也可以实现：

logger.add("file.log", compression="zip") 

'''
通过上面的配置，我们指定了日志文件的压缩格式为 zip 。
异常捕获
loguru 不仅可以记录日志，还可以捕获异常信息，这个可以帮助我们更好地追溯错误原因。
在 loguru 模块中，我们通常有两种异常捕获方式：通过 catch 装饰器捕获和通过 exception 方法捕获。
catch 装饰器捕获异常
我们来看一个例子：
'''

@logger.catch
def a_function(x):
    return 1 / x

a_function(0)

#exception 方法捕获异常
#我们直接看例子：

def b_function1(x):
    try:
        return 1 / x
    except ZeroDivisionError:
        logger.exception("exception!!!")

b_function1(0)

