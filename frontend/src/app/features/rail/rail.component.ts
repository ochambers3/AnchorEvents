import { Component, signal } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-rail',
  standalone: true,
  imports: [NgFor, MatIconModule, MatButtonModule],
  templateUrl: './rail.component.html',
  styleUrl: './rail.component.css'
})
export class RailComponent {
  navItems = signal([
    { icon: 'nightlife', label: 'Events' },
    { icon: 'today', label: 'Dates' },
    { icon: 'next_week', label: 'Weekdays' },
    { icon: 'location_city', label: 'Cities' },
    { icon: 'format_list_numbered', label: 'Quantity' },
  ]);

  activeItem = signal<string | null>(null);

  toggle(label: string) {
    this.activeItem.set(this.activeItem() === label ? null : label);
    console.log('Toggled:', label);
    // Optionally emit an output or call a signal/store
  }

  doSomething() {
    console.log("Doing things");
  }
}
