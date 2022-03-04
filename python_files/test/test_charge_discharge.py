from src import charge_from_grid

march_3rd = {
    'average': 2.19,
    'off_peak_1': 1.63,
    'off_peak_2': 2.08,
    'peak': 2.11
}

march_4th = {
    'average': 2.67,
    'off_peak_1': 2.41,
    'off_peak_2': 2.13,
    'peak': 2.78
}

day_0 = {
    'average': 1.2,
    'off_peak_1': 0.63,
    'off_peak_2': 2.08,
    'peak': 1.61
}

def test__march_4th__0000__real__do_charge():
    current_price = 1.73
    current_hour = 0
    do_charge = charge_from_grid.allow_factor(
        current_hour=current_hour,
        current_price=current_price,
        day_average=march_4th['average'],
        off_peak_1=march_4th['off_peak_1'],
        off_peak_2=march_4th['off_peak_2'], 
        peak=march_4th['peak'] 
    ) 
    assert do_charge > 1

def test__march_4th__0000___do_not_charge():
    current_price = 1.9
    current_hour = 4
    do_charge = charge_from_grid.allow_factor(
        current_hour=current_hour,
        current_price=current_price,
        day_average=march_4th['average'],
        off_peak_1=march_4th['off_peak_1'],
        off_peak_2=march_4th['off_peak_2'], 
        peak=march_4th['peak'] 
    ) 
    assert do_charge < 1

def test__march_4th__0100__do_charge():
    current_price = 1.67
    current_hour = 1
    do_charge = charge_from_grid.allow_factor(
        current_hour=current_hour,
        current_price=current_price,
        day_average=march_4th['average'],
        off_peak_1=march_4th['off_peak_1'],
        off_peak_2=march_4th['off_peak_2'], 
        peak=march_4th['peak'] 
    )
    assert do_charge > 1

def test__march_3rd__1500__do_charge():
    current_price = 1.6
    current_hour = 15
    do_charge = charge_from_grid.allow_factor(
        current_hour=current_hour,
        current_price=current_price,
        day_average=march_3rd['average'],
        off_peak_1=march_3rd['off_peak_1'],
        off_peak_2=march_3rd['off_peak_2'], 
        peak=march_3rd['peak'] 
    ) 
    assert do_charge > 1

def test__mars_third__2300__real__do_not_charge():
    current_price = 1.82
    current_hour = 23
    do_charge = charge_from_grid.allow_factor(
        current_hour=current_hour,
        current_price=current_price,
        day_average=march_3rd['average'],
        off_peak_1=march_3rd['off_peak_1'],
        off_peak_2=march_3rd['off_peak_2'], 
        peak=march_3rd['peak'] 
    ) 
    assert do_charge < 1

def test__march_3rd__0800__do_not_charge():
    current_price = 2.55
    current_hour = 8
    do_charge = charge_from_grid.allow_factor(
        current_hour=current_hour,
        current_price=current_price,
        day_average=march_3rd['average'],
        off_peak_1=march_3rd['off_peak_1'],
        off_peak_2=march_3rd['off_peak_2'], 
        peak=march_3rd['peak'] 
    ) 
    assert do_charge < 1

def test__day_0__2100__do_not_charge():
    current_price = 2.1
    current_hour = 21
    do_charge = charge_from_grid.allow_factor(
        current_hour=current_hour,
        current_price=current_price,
        day_average=march_3rd['average'],
        off_peak_1=march_3rd['off_peak_1'],
        off_peak_2=march_3rd['off_peak_2'], 
        peak=march_3rd['peak'] 
    ) 
    assert do_charge < 1

def test__day_0__2100__do_charge__price_low():
    current_price = 1.6
    current_hour = 21
    do_charge = charge_from_grid.allow_factor(
        current_hour=current_hour,
        current_price=current_price,
        day_average=march_3rd['average'],
        off_peak_1=march_3rd['off_peak_1'],
        off_peak_2=march_3rd['off_peak_2'], 
        peak=march_3rd['peak'] 
    ) 
    assert do_charge > 1
