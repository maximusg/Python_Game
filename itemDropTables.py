#filename: itemDropTables.py
'''
purpose: create tables linking items to their drop rates, to be used when creating enemies. Upon enemy
         death, the enemy will run the getDrop() method, which will examine one of these drop tables to see
         whether an item will drop or not.

         You don't have to ensure that the probabilities are exactly 1:
         the remaining percentage will mean nothing will drop. Example - the common itemDropTable specifies that
         a coin will drop 40% of the time, a powerup will drop 10% of the time, and the remaining 50% of the time
         nothing will drop.

         Just make sure your probabilities don't add up to more than 1
'''

common = (('coin', 0.4),('powerup', 0.1))

rare = (('coin', 0.2), 'powerup', 0.8)