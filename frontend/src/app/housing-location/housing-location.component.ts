import { Component, input } from '@angular/core';
import { HousingLocationInfo } from '../housinglocation';

@Component({
  selector: 'app-housing-location',
  standalone: true,
  template: `
    <section class="listing">
      <img
        class="listing-photo"
        [src]="housingLocation().photo"
        alt="Exterior photo of {{ housingLocation().name }}"
        crossorigin
      />
      <h2 class="listing-heading">{{ housingLocation().name }}</h2>
      <p class="listing-location">{{ housingLocation().city }}, {{ housingLocation().state }}</p>
    </section>
  `,
  styleUrls: ['./housing-location.component.css'],
  // standalone: true,
  // imports: [],
  // templateUrl: './housing-location.component.html',
  // styleUrl: './housing-location.component.css'
})
export class HousingLocationComponent {
  housingLocation = input.required<HousingLocationInfo>();
}
