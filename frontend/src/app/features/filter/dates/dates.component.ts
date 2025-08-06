import { Component, Input, Type } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { PopupService, SearchCriteriaService } from '../../../housing.service';
import { MatButtonModule } from '@angular/material/button';
import { MatDateRangePicker } from '@angular/material/datepicker';

@Component({
  selector: 'app-dates',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, MatDatepickerModule, MatNativeDateModule, FormsModule, ReactiveFormsModule, MatButtonModule, MatDateRangePicker],
  templateUrl: './dates.component.html',
  // styleUrl: './dates.component.css'
  styleUrl: '../pop-up.css'
})
export class DatesComponent {
  @Input() contentComponent!: Type<any>;

  startDate: Date | null = null;
  endDate: Date | null = null;

  constructor(private searchCriteria: SearchCriteriaService, private popupService: PopupService) {}

  saveDates() {
    this.searchCriteria.setDates(this.startDate, this.endDate);
    this.popupService.closePopup();
    console.log('Dates:', this.startDate, this.endDate);
  }
}
