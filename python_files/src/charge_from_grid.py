    
threshold_factor = 1.8    # The average price should be twice as high as the current price
    
def allow_factor(current_hour, current_price, day_average, off_peak_1, off_peak_2, peak):
    local_avg = get_local_average(current_hour, off_peak_1, peak, off_peak_2)                
    day_average_factor = day_average / current_price             
    local_average_factor = local_avg / current_price
    return day_average_factor * local_average_factor / threshold_factor

def get_local_average(current_hour, avg1, avg2, avg3):
    if current_hour < 8:
        return avg1
    if current_hour >= 8:
        return avg2
    if current_hour >= 20:
        return avg3
    