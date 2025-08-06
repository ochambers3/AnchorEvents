import { Component, Input, Type } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { FormBuilder, FormsModule, ReactiveFormsModule, FormGroup, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { PopupService, SearchCriteriaService } from '../../../housing.service';
import { MatButtonModule } from '@angular/material/button';
import { MatDateRangePicker } from '@angular/material/datepicker';

@Component({
  selector: 'app-dates',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, MatDatepickerModule, MatNativeDateModule, FormsModule, ReactiveFormsModule, MatButtonModule, MatDateRangePicker, CommonModule],
  templateUrl: './dates.component.html',
  // styleUrl: './dates.component.css'
  styleUrl: '../pop-up.css'
})
export class DatesComponent {
  dateForm: FormGroup;
  
  constructor(private fb: FormBuilder, private searchCriteria: SearchCriteriaService, private popupService: PopupService) {
    this.dateForm = this.fb.group({
      // array of validator methods. Use Validators.required if required
      startDate: [null, [this.todayValidator]],
      endDate: [null, [this.todayValidator]]
    }, { validators: [this.dateRangeValidator] });
  }

  // Display range of dates
  get dateRangeDisplay(): string {
    const startDate = this.dateForm.get('startDate')?.value;
    const endDate = this.dateForm.get('endDate')?.value;
    
    if (startDate && endDate) {
      return `${this.formatDate(startDate)} - ${this.formatDate(endDate)}`;
    } else if (startDate) {
      return `Start: ${this.formatDate(startDate)}`;
    } else if (endDate) {
      return `End: ${this.formatDate(endDate)}`;
    }
    return '';
  }

  // Format the date
  private formatDate(date: Date): string {
    return new Intl.DateTimeFormat('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    }).format(date);
  }

  // Custom validator: date must be today or later
  todayValidator(control: AbstractControl): ValidationErrors | null {
    if (!control.value) return null;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return control.value < today ? { today: true } : null;
  }

  // Custom validator: endDate must be after startDate
  dateRangeValidator(group: AbstractControl): ValidationErrors | null {
    const startDate = group.get('startDate')?.value;
    const endDate = group.get('endDate')?.value;
    
    if (!startDate || !endDate) return null;
    return endDate < startDate ? { invalidOrder: true } : null;
  }

  // Error message helper
  getErrorMessage(field: string): string {
    const control = this.dateForm.get(field);
    if (!control?.errors) return '';

    if (control.errors['required']) return `${field} is required`;
    if (control.errors['today']) return 'Date must begin after today';
    if (this.dateForm.errors?.[field === 'endDate' ? 'invalidOrder' : '']) {
      return 'End date must be after start date';
    }
    return '';
  }

  saveDates() {
    if (this.dateForm.valid) {
      const { startDate, endDate } = this.dateForm.value;
      console.log('Valid dates:', { startDate, endDate });
      this.searchCriteria.setDates(startDate, endDate);
      this.popupService.closePopup();
      // Handle save logic
    } else {
      console.log('Form is invalid');
      this.dateForm.markAllAsTouched();
    }
  }

  get startDate() { return this.dateForm.get('startDate'); }
  get endDate() { return this.dateForm.get('endDate'); }
}
