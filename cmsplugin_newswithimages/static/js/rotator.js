;(function($){
	var defaults = {
        nextSelector: null,
	    prevSelector: null,
		maxSlides: 10,
        rotateInterval:5000, 
    }

    $.fn.divSlider = function(options){
        if(this.length == 0) return;
        
        var dslider = {};

        var self = this;

        timer: false;
        active: false;

        this.init = function(options){
            dslider.settings = $.extend({}, defaults, options);
            dslider.children = self.children();
            dslider.numberOfChildren = dslider.children.length;


            var sum=0;
            self.children().each( function(){ sum += $(this).height(); });
            self.height( sum );


            if (dslider.settings.maxSlides > dslider.numberOfChildren) {
                dslider.settings.maxSlides = dslider.numberOfChildren;
            }
            dslider.working = false;

            var activeChildren = self.children().slice(0, dslider.settings.maxSlides ); 
            //activeChildren.css("display", "block");
            
            var sum=0;
            activeChildren.each( function(){ sum += $(this).height(); });
            self.css( 'height', sum+'px' );


            self.children().slice(dslider.settings.maxSlides , dslider.numberOfChildren).hide();
      
            if( dslider.numberOfChildren > dslider.settings.maxSlides ) {
                self.addControls();
                self.start();
            }
          
        }

        this.next = function() {            
            var child = self.children().eq(0).hide();
            child.appendTo(self); 

            self.children().eq(dslider.settings.maxSlides-1).show();  
        };


        this.back = function() {
            self.children().eq(dslider.settings.maxSlides-1).hide();
            self.children().eq(-1).prependTo(self); 

            self.children().eq(0).show();  
        }

        this.addControls = function() {
            if(dslider.settings.nextSelector){
				$(dslider.settings.nextSelector).click('click', nextSelectorClick);
			}

            if(dslider.settings.backSelector){
				$(dslider.settings.backSelector).bind('click', backSelectorClick);
			}
        };

        this.start = function() {
            if ( self.timer || self.active ){
                return false;
            }
            
            self.active = true;
            self.timer = setInterval(self.next, dslider.settings.rotateInterval);
        };

            
        this.stop = function() {
            clearInterval(self.timer);
            self.timer = null;
            self.active = false;
        };

        var nextSelectorClick = function() {
            self.stop();
            self.next();
            self.start();
        };

        var backSelectorClick = function() {
            self.stop();
            self.back();
            self.start();
        };

        self.init(options);

        return this
    };

})(jQuery);



