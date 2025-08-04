import { Component, Input, Type } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SearchCriteriaService } from '../../../housing.service';

@Component({
  selector: 'app-dates',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, MatDatepickerModule, MatNativeDateModule, FormsModule, ReactiveFormsModule],
  templateUrl: './dates.component.html',
  styleUrl: './dates.component.css'
})
export class DatesComponent {
  @Input() contentComponent!: Type<any>;

  startDate: Date | null = null;
  endDate: Date | null = null;

  constructor(private searchCriteria: SearchCriteriaService) {}

  saveDates() {
    if (this.startDate && this.endDate) {
      this.searchCriteria.setDates(this.startDate, this.endDate);
    }
  }
}
