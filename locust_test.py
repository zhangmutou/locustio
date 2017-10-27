# locust_test.py
# from locust import HttpLocust, TaskSet, task

# class TestFlask(TaskSet):

# 	@task(1)
# 	def task1(self):
# 		self.client.post('/a/2')

# 	@task(1)
# 	def task2(self):
# 		self.client.post('/b/5')

# 	# @task(1)
# 	# def task3(self):
# 	# 	self.client.post('/4')

# class Test(HttpLocust):
# 	task_set = TestFlask
# 	min_wait = 5000
# 	max_wait = 5000

# 	name = 'TestFlask'
# 	host = 'http://127.0.0.1:8787'

# from locust import Locust, TaskSet, task

# class stay(TaskSet):
#     @task(3)
#     def readBook(self):
#         print('I am reading a book.')

#     @task(7)
#     def listenMusic(self):
#         print('I am listening to music.')

#     @task(1)
#     def logOut(self):
#         self.interrupt()

# class UserTask(TaskSet):
#     tasks = {stay:1}

#     @task(2)
#     def leave(self):
#         print('I don not like this page.')

# class User(Locust):
#     task_set = UserTask

from core import HttpLocust, Locust, TaskSet, task, events

import random, traceback

def on_request_success(request_type, name, response_time, response_length):
    print('Type: %s, Name: %s, Time: %fms, Response Length: %d' % \
            (request_type, name, response_time, response_length))

def on_request_failure(request_type, name, response_time, exception):
    print('Type: %s, Name: %s, Time: %fms, Reason: %r' % \
            (request_type, name, response_time, exception))

def on_locust_error(locust_instance, exception, tb):
    print("%r, %s, %s" % (locust_instance, exception, "".join(traceback.format_tb(tb))))

def on_hatch_complete(user_count):
    print("Haha, Locust have generate %d users" % user_count)

def on_quitting():
    print("Locust is quiting")

events.request_success += on_request_success
events.request_failure += on_request_failure
events.locust_error += on_locust_error
events.hatch_complete += on_hatch_complete
events.quitting += on_quitting


class UserTask(TaskSet):
    @task(5)
    def job1(self):
        with self.client.get('/', catch_response = True) as r:
            if random.choice([0, 1]):
                r.success()
            else:
                r.failure('0')

    @task(1)
    def job2(self):
        raise Exception("Mars Loo's test")

class User(HttpLocust):
    task_set = UserTask
    min_wait = 3000
    max_wait = 5000
    host = 'http://www.baidu.com'

