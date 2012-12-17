;(function($){
	var defaults = {
        nextSelector: null,
	    prevSelector: null,
		maxSlides: 10,
        rotateInterval:5000, 
    }

    $.fn.divSlider = function(options){
        if(this.length == 0) return;
        
        /* create a namespace */
        var dslider = {};
        /* using self instead of this */
        var self = this;

        this.init = function(options){
            var children = self.children();
            dslider.settings = $.extend({}, defaults, options);
            // save the number of children, this code doesn't change it
            dslider.numberOfChildren = children.length;
            dslider.active = false;
            dslider.timer = false;

            if (dslider.settings.maxSlides > dslider.numberOfChildren) {
                dslider.settings.maxSlides = dslider.numberOfChildren;
            }
            
            var activeChildren = children.slice(0, dslider.settings.maxSlides ); 
            
            //fix the height of the container to avoid resizing while moving 
            //inside element
            var sum=0;
            activeChildren.each( function(){ sum += $(this).height(); });
            self.css( 'height', sum+'px' );
            
            //hide children that appear after the maxSlides parameter
            self.children().slice(dslider.settings.maxSlides , dslider.numberOfChildren).hide();
      
            if( dslider.numberOfChildren > dslider.settings.maxSlides ) {
                self.addControls();
                self.start();
            }
          
        }

        /*move slide forward*/
        this.next = function() {            
            var child = self.children().eq(0).hide();
            child.appendTo(self); 

            self.children().eq(dslider.settings.maxSlides-1).show();  
        };

        /*move slide backward*/
        this.back = function() {
            self.children().eq(dslider.settings.maxSlides-1).hide();
            self.children().eq(-1).prependTo(self); 

            self.children().eq(0).show();  
        }

        /*check if controllers are specified and eventually asign
          the control function to each controller*/
        this.addControls = function() {
            if(dslider.settings.nextSelector){
				$(dslider.settings.nextSelector).click('click', nextSelectorClick);
			}

            if(dslider.settings.backSelector){
				$(dslider.settings.backSelector).bind('click', backSelectorClick);
			}
        };

        /*start rotating element*/
        this.start = function() {
            if ( self.timer || self.active ){
                return false;
            }
            
            self.active = true;
            self.timer = setInterval(self.next, dslider.settings.rotateInterval);
        };

        /*stop rotating element*/
        this.stop = function() {
            clearInterval(self.timer);
            self.timer = null;
            self.active = false;
        };

        /*function next that is assigned for optional controller*/
        var nextSelectorClick = function() {
            self.stop();
            self.next();
            self.start();
        };

        /*function back that is assigned for optional controller*/
        var backSelectorClick = function() {
            self.stop();
            self.back();
            self.start();
        };

        /*initialize divSlider*/
        self.init(options);

        return this
    };

})(jQuery);



