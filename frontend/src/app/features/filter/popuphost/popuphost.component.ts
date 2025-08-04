import { Component, Input, Type } from '@angular/core';

@Component({
  selector: 'app-popup-host',
  standalone: true,
  imports: [],
  // templateUrl: './popuphost.component.html',
  template: `@if (contentComponent) {
    <ng-container *ngComponentOutlet="contentComponent"></ng-container>
  }`,
  styleUrl: './popuphost.component.css'
})
export class PopupHostComponent {
  @Input() contentComponent!: Type<any>;
}
