import random
import cProfile
cProfile.run("""for i in range(1000000):
  random.random()""")
cProfile.run("""for i in range(1000000):
  random.randint(1,4)""")
