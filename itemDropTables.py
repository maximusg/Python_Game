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

#common = (('coin', 0.1),('spitfire_powerup', 0.05))#, ('spitfire_powerup', 0.3))


common = (
    ('coin', 0.1),
    ('spitfire_powerup', 0.05),
    ('wavebeam_powerup', 0.05),
    ('chargeShot_powerup', 0.05),
    ('bomb_item', 0.1)
        )

#guaranteed to drop a spitfire powerup every time
spitfire = (

    ('spitfire_powerup', 1)
)

#guaranteed to drop a chargeShot powerup every time

chargeShot = (

    ('chargeShot_powerup', 1)
)

#guaranteed to drop a waveBeam powerup every time
waveBeam = (

    ('wavebeam_powerup', 1)
)

#use the empty itemDropTable to never allow items to drop from enemies
empty = None


DTDic = {
    'DTcommon': common,
    'DTspitfire': spitfire,
    'DTchargeShot': chargeShot,
    'DTwaveBeam': waveBeam,
    'DTempty': empty,
    'DThealth': common
}