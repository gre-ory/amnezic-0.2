
// //////////////////////////////////////////////////
// Button

function Button( id ) {
    this.id = id;
    this.element = document.getElementById( this.id );
    if ( !this.element ) {
        console.log( 'warning: element ' + this.id + ' not found!' );
    }
}

Button.prototype.on_click = function( on_click ) {
    if ( this.element ) {
        this.element.onclick = on_click;
    }
    return this;
}

Button.prototype.enable = function() {
    if ( this.element ) {
        this.element.removeAttribute( "disabled" );
        if ( this.element._onclick ) {
            this.element.onclick = this.element._onclick;
            this.element._onclick = null;
        }
    }
    return this;
}

Button.prototype.disable = function() {
    if ( this.element ) {
        this.element.setAttribute( "disabled", true );
        if ( this.element.onclick ) {
            this.element._onclick = this.element.onclick;
            this.element.onclick = null;
        }
    }
    return this;
}

// //////////////////////////////////////////////////
// Player

function Player( base_id ) {
    this.base_id = base_id || 'player';
    this.id = this.base_id.concat( "-audio" );
    this.volume_before_mute = null;
    this.muted = false;
    this.source = null;
    this.paused = true;
    this.hidden = true;
    this.auto_start = false;
    this.loop = false;
    
    this.init();
}

// //////////////////////////////////////////////////
// init

Player.prototype.init = function() {
    this.audio = document.getElementById( this.id );
    if ( !this.audio ) {
        console.log( 'warning: element ' + this.id + ' not found!' );
        return;
    }
    this.audio.volume = 0.5;
    this.audio.paused = false;
    this.audio.muted = false;
    
    this.audio.setAttribute( "hidden", this.hidden ? "true" : "false" );
    this.audio.setAttribute( "autostart", this.auto_start ? "true" : "false" );
    this.audio.setAttribute( "loop", this.loop ? "true" : "false" );

    this.button_play  = new Button( this.base_id.concat( "-play" ) ).on_click( this.play.bind( this ) );
    this.button_pause = new Button( this.base_id.concat( "-pause" ) ).on_click( this.pause.bind( this ) );
    this.button_stop = new Button( this.base_id.concat( "-stop" ) ).on_click( this.stop.bind( this ) );
    this.button_down = new Button( this.base_id.concat( "-down" ) ).on_click( this.volume_down.bind( this ) );
    this.button_mute = new Button( this.base_id.concat( "-mute" ) ).on_click( this.volume_mute.bind( this ) );
    this.button_up = new Button( this.base_id.concat( "-up" ) ).on_click( this.volume_up.bind( this ) );
    
    console.log( '{ paused: ' + this.audio.paused + ', muted: ' + this.audio.muted + ', source: ' + this.source + ' }' );
    this.button_play.disable();
    this.button_pause.disable();
    this.button_stop.disable();
    this.button_down.disable();
    this.button_mute.disable();
    this.button_up.disable();
}

// //////////////////////////////////////////////////
// play

Player.prototype.load = function( source ) {
    this.source = source;
    if ( this.audio ) {
        this.audio.setAttribute( "src", this.source );
        this.audio.load();
    }
    this.play();
}

Player.prototype.play = function() {
    if ( this.audio ) {
        this.audio.play();
    }
    this.button_play.disable();
    this.button_pause.enable();
    this.button_stop.enable();
    this.button_down.enable();
    this.button_mute.enable();
    this.button_up.enable();
}

Player.prototype.pause = function() {
    if ( this.audio ) {
        this.audio.pause();
    }
    this.button_play.enable();
    this.button_pause.disable();
    this.button_stop.disable();
    this.button_down.disable();
    this.button_mute.disable();
    this.button_up.disable();
}

Player.prototype.stop = function() {
    if ( this.audio ) {
        this.audio.pause();
    }
    this.button_play.enable();
    this.button_pause.disable();
    this.button_stop.disable();
    this.button_down.disable();
    this.button_mute.disable();
    this.button_up.disable();
}

// //////////////////////////////////////////////////
// volume

Player.prototype.volume_up = function() {
    if ( this.audio.volume > 0.9 ) {
        this.audio.volume = 1.0;
        this.button_up.disable();
    }
    else {
        this.audio.volume = this.audio.volume + 0.1;
        this.button_down.enable();
        this.button_mute.enable();
    }
}

Player.prototype.volume_down = function() {
    if ( this.audio.volume < 0.1 ) {
        this.audio.volume = 0.0;
        this.button_down.disable();
        this.button_mute.disable();
    }
    else {
        this.audio.volume = this.audio.volume - 0.1;
        this.button_up.enable();
    }
}

Player.prototype.volume_mute = function() {
    if ( this.audio ) {
        this.audio.muted = !this.audio.muted;
        if ( this.audio.muted ) {
            this.button_down.disable();
            this.button_up.disable();
        }
        else {
            this.button_down.enable();
            this.button_up.enable();
        }
    }
}
 