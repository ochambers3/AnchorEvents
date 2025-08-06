import { Component, signal, Type } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { CitiesComponent } from '../filter/cities/cities.component';
import { PopupService } from '../../housing.service';
import { SearchCriteriaService } from '../../housing.service';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DatesComponent } from '../filter/dates/dates.component';
import { EventsComponent } from '../filter/events/events.component';

@Component({
  selector: 'app-rail',
  standalone: true,
  imports: [MatIconModule, MatButtonModule],
  templateUrl: './rail.component.html',
  styleUrl: './rail.component.css'
})
export class RailComponent {
  constructor(private popupService: PopupService, private searchCriteria: SearchCriteriaService) {
    this.popupService.popupClosed$.pipe(takeUntilDestroyed()).subscribe(() => {
      this.activeItem.set(null);
    });
  }

  navItems = signal([
    { icon: 'nightlife', label: 'Events', component: EventsComponent },
    { icon: 'today', label: 'Dates', component: DatesComponent },
    { icon: 'next_week', label: 'Weekdays', component: null },
    { icon: 'location_city', label: 'Cities', component: CitiesComponent },
    { icon: 'format_list_numbered', label: 'Quantity', component: null },
  ]);

  activeItem = signal<string | null>(null);

  toggle(label: string, event: MouseEvent) {
    const wasActive = this.activeItem() === label;
    this.activeItem.set(wasActive ? null : label);

    if (!wasActive) {
      const item = this.navItems().find(item => item.label === label);
      if (item?.component) {
        this.openPopup(item.component, event)
      }
    }
    // this.openPopup(label, event);
  }

  doSomething() {
    console.log("Doing things");
  }

  openPopup(component: Type<any>, event: MouseEvent) {
    const origin = event.target as HTMLElement;
    this.popupService.openPopup(component, origin);
  }

  sendRequest() {
    this.searchCriteria.sendRequest();
  }
}
