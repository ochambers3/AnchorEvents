import { Component, signal, Type } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { CitiesComponent } from '../filter/cities/cities.component';
import { PopupService } from '../../housing.service';

@Component({
  selector: 'app-rail',
  standalone: true,
  imports: [MatIconModule, MatButtonModule],
  templateUrl: './rail.component.html',
  styleUrl: './rail.component.css'
})
export class RailComponent {
  constructor(private popupService: PopupService) {}

  navItems = signal([
    { icon: 'nightlife', label: 'Events', component: null },
    { icon: 'today', label: 'Dates', component: null },
    { icon: 'next_week', label: 'Weekdays', component: null },
    { icon: 'location_city', label: 'Cities', component: CitiesComponent },
    { icon: 'format_list_numbered', label: 'Quantity', component: null },
  ]);

  activeItem = signal<string | null>(null);

  toggle(label: string, event: MouseEvent) {
    const wasActive = this.activeItem() === label;
    this.activeItem.set(wasActive ? null : label);
    console.log('Was active: ', wasActive);
    console.log('Got event: ', event);

    if (!wasActive) {
      console.log('Was Active was false')
      const item = this.navItems().find(item => item.label === label);
      console.log('Item component', item, item?.component)
      if (item?.component) {
        console.log('opening popup');
        this.openPopup(item.component, event)
      }
    }
    console.log('Toggled:', label);
    // this.openPopup(label, event);
  }

  doSomething() {
    console.log("Doing things");
  }

  openPopup(component: Type<any>, event: MouseEvent) {
    console.log('git rail component and evnet: ', component, event)
    const origin = event.target as HTMLElement;
    this.popupService.openPopup(component, origin);
  }

  openCitySelector(event: MouseEvent) {
    console.log('Opening city selector');
    const origin = event.target as HTMLElement;
    this.popupService.openPopup(CitiesComponent, origin);
  }
  
  
}
