"""
Cookie Clicker Simulator
"""

import simpleplot
import simplegui
# Used to increase the timeout, if necessary
import codeskulptor
import math

codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._current_time=0.0
        self._current_cps=1.0
        self._current_cookies=self._current_time*self._current_cps
        self._total_cookies_produced=0.0
        self._history=[(0.0,None,0.0,0.0)]
       
        
    def __str__(self):
        """
        Return human readable state
        """
        hrs= "\nTime : " + str(self._current_time)+ "\n"
        hrs=hrs+ "Current cookies : " + str(self._current_cookies)+ "\n"
        hrs=hrs+ "CPS : " + str(self._current_cps)+ "\n"
        hrs=hrs+"Total cookies : " + str(self._total_cookies_produced) + "\n"
        return hrs
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def set_cookies(self,cookies):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        self._current_cookies=cookies
    
    def set_total_cookies(self,cookies):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        self._total_cookies_produced=self._total_cookies_produced+cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def set_time(self, current_time):
        """
        Get current time

        Should return a float
        """
        self._current_time=current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        timer1=0.0
    
        if self._current_cookies == cookies:
            timer1=0.0
     
        elif self._current_cookies < cookies:
            difference=cookies-self._current_cookies
            timer1=math.ceil(difference/self.get_cps())

        elif self._current_cookies >= cookies:
            timer1=0.0

        return timer1
    
 
    
    def wait(self, delay):
        """
        Wait for given amount of time and update state
        Should do nothing if time <= 0
        """
        if delay >0 :
            self._current_time=self._current_time+delay
            self.set_cookies(self._current_cookies+(delay*self._current_cps))
            self.set_total_cookies(self.get_cookies())

    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        bought=0
        
        
        if self._current_cookies >= cost:
            self._current_cookies=self._current_cookies-cost
            self._current_cps=self.get_cps() + additional_cps
            self._history.append((self._current_time,item_name,cost,self._total_cookies_produced))
            bought=1
        else:
            print "cannot afford"
 
        return bought    

def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    state=ClickerState()
    build_info_clone=build_info.clone()
    count=state.get_time()
    while  count <= duration :

        item= strategy(state.get_cookies(),state.get_cps(),duration-count,build_info_clone)
            
        if item == None :
           state.wait(duration)
           break
    
        time_required=state.time_until(build_info.get_cost(item))
     
        if (state.get_time()+time_required) > duration :
            state.set_cookies(state.get_cookies()+((duration-state.get_time())*state.get_cps()))
            state.set_time(state.get_time()+(duration-state.get_time()))
            state.set_total_cookies(state.get_cookies())
            break
        else:
            state.wait(time_required)
        
        
        flag=state.buy_item(item,build_info.get_cost(item),build_info.get_cps(item))   
        
        if flag==1:
            build_info.update_item(item)
   
        count= state.get_time()
 

    return state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always return the cheapest policy
    """
    cheap_build_clone= build_info.clone()
    itemlistcheap=cheap_build_clone.build_items()
    total_cookies_cheap= cookies + (time_left*cps)
    minimum=float(total_cookies_cheap)
    result_cheap=''
    for item in itemlistcheap:	
        temp_cheap=cheap_build_clone.get_cost(item)
        #print item,temp_cheap,total_cookies_cheap,minimum
        if temp_cheap <= total_cookies_cheap  :
            #print item,"Hello",minimum,temp_cheap
            if temp_cheap <= minimum :
                print item, temp_cheap, minimum
                minimum=temp_cheap
                result_cheap= item
           
    if result_cheap == '' :
        return None
    else :
        return result_cheap

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Always return the most expensive policy
    """
    exp_build_clone= build_info.clone()
    itemlist=exp_build_clone.build_items()
    total_cookies= cookies + (time_left*cps)
    maximum=0.0
    result=''
    for item in itemlist:	
        temp=exp_build_clone.get_cost(item)
        if total_cookies >= temp and temp > maximum :
          maximum=temp
          result= item
           
    if result == '' :
        return None
    else :
        return result

def strategy_best(cookies, cps, time_left, build_info):
    """
    Always return the best policy
    """
    return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy_cursor)
    print strategy_name, ":", state
    #print strategy_cheap(500000.0, 1.0, 5.0, provided.BuildInfo({'C': [50000.0, 3.0], 'B': [500.0, 2.0],'A': [5.0, 1.0]}, 1.15))
    #print strategy_expensive(500000.0, 1.0, 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))
    #print strategy_cheap(2.0, 1.0, 1.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))
    #print strategy_cheap(1.0, 3.0, 17.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))
    # Plot total cookies over time
    #print strategy_cheap(0.0, 1.0, 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)) 
    #state=simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 15, strategy_cursor)
    #print strategy_name, ":", state
    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it
    #print strategy_cheap(500000.0, 1.0, 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)) 
    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    
