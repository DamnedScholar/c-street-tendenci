import { Controller } from 'stimulus';
import StimulusReflex from 'stimulus_reflex';

export default class extends Controller {
  static targets = ['tag-filter', 'grid', 'listing']

  initialize() {
    this.element['isotope'] = this
    
    this.iso = new Isotope( '.grid', {
      itemSelector: '.element-item',
      layoutMode: 'fitRows'
    });
  }

  connect() {
    StimulusReflex.register(this)
  }

  filter(event) {
    filterFn = event.currentTarget.getAttribute('data-filter')

    this.iso.arrange({
      filter: this[filterFn](event)
    })
  }

  filterTags(event) {
    var taglist = this.gridTarget.querySelector('.tags').innerText
    tag = new RegExp(event.target.innerText)
    return taglist.match( tag )
  }

  filterOpen(status) {
    var status = itemElem.querySelector('.status').innerText
    return status.match( /open/ )
}

  filterService(service) {
    this.iso.arrange({
      // item element provided as argument
      filter: function( itemElem ) {
        var service = itemElem.querySelector('.tags').innerText
        return service.match( /ium$/ )
      }
    })
  }
}

// filter functions
var filterFns = {
  // show if number is greater than 50
  numberGreaterThan50: function( itemElem ) {
    var number = itemElem.querySelector('.number').textContent;
    return parseInt( number, 10 ) > 50;
  },
  // show if name ends with -ium
  ium: function( itemElem ) {
    var name = itemElem.querySelector('.name').textContent;
    return name.match( /ium$/ );
  }
};

// bind filter button click
var filtersElem = document.querySelector('.filters-button-group');
filtersElem.addEventListener( 'click', function( event ) {
  // only work with buttons
  if ( !matchesSelector( event.target, 'button' ) ) {
    return;
  }
  var filterValue = event.target.getAttribute('data-filter');
  // use matching filter function
  filterValue = filterFns[ filterValue ] || filterValue;
  iso.arrange({ filter: filterValue });
});

// change is-checked class on buttons
var buttonGroups = document.querySelectorAll('.button-group');
for ( var i=0, len = buttonGroups.length; i < len; i++ ) {
  var buttonGroup = buttonGroups[i];
  radioButtonGroup( buttonGroup );
}

function radioButtonGroup( buttonGroup ) {
  buttonGroup.addEventListener( 'click', function( event ) {
    // only work with buttons
    if ( !matchesSelector( event.target, 'button' ) ) {
      return;
    }
    buttonGroup.querySelector('.is-checked').classList.remove('is-checked');
    event.target.classList.add('is-checked');
  });
}
