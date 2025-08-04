import { Component } from '@angular/core';
import { PopupService, SearchCriteriaService } from '../../../housing.service';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-cities',
  standalone: true,
  imports: [MatIconModule, MatChipsModule, FormsModule, MatInputModule, MatFormFieldModule, MatButtonModule],
  // templateUrl: './cities.component.html',
  template: `
    <div class="cities-popup">
      <h3>Select Cities</h3>
      <mat-form-field appearance="outline" class="full-width">
        <mat-label>Cities</mat-label>
        <input matInput [(ngModel)]="city" (keyup.enter)="addCity()" placeholder="Enter city name" />
      </mat-form-field>
      
      @if (cities.length > 0) {
        <div class="chips-container">
          <mat-chip-set>
            @for (c of cities; track c) {
              <mat-chip (removed)="removeCity(c)" removable="true">
                {{ c }}
                <mat-icon matChipRemove>cancel</mat-icon>
              </mat-chip>
            }
          </mat-chip-set>
        </div>
      }
      
      <div class="actions">
        <button mat-raised-button (click)="save()">Save Cities</button>
      </div>
    </div>
  `,
  // styleUrl: './cities.component.css'
  styleUrl: '../pop-up.css'
})
export class CitiesComponent {
  cities: string[] = [];
  city: string = '';

  constructor(private searchCriteria: SearchCriteriaService, private popupService: PopupService) {
    const existing = this.searchCriteria.getCriteria();
    this.cities = [...existing.cities]
  }

  addCity() {
    if (this.city.trim() && !this.cities.includes(this.city.trim())) {
      this.cities.push(this.city.trim());
      this.city = '';
    }
  }

  removeCity(c: string) {
    this.cities = this.cities.filter(x => x !== c);
  }

  save() {
    this.searchCriteria.setCities(this.cities);
    this.popupService.closePopup();
    console.log('Cities saved:', this.cities);
  }
}
