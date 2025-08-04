import { Injectable, Injector, Type } from '@angular/core';
import { HousingLocationInfo } from './housinglocation';
import { Overlay, OverlayRef } from '@angular/cdk/overlay';
import { ComponentPortal } from '@angular/cdk/portal';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HousingService {
  url = 'http://localhost:3000/locations';

  async getAllHousingLocations(): Promise<HousingLocationInfo[]> {
    const data = await fetch(this.url);
    return (await data.json()) ?? [];
  }

  async getHousingLocationById(id: number): Promise<HousingLocationInfo | undefined> {
    const data = await fetch(`${this.url}?id=${id}`);
    const locationJson = await data.json();
    return locationJson[0] ?? {};
  }

  submitApplication(firstName: string, lastName: string, email: string) {
    console.log(
      `Homes application received: fistname: ${firstName}, lastName: ${lastName}, email: ${email}.`
    );
  }
}

@Injectable({ providedIn: 'root' })
export class PopupService {
  private currentOverlayRef: OverlayRef | null = null;
  private popupClosedSubject = new Subject<void>();
  popupClosed$ = this.popupClosedSubject.asObservable();

  constructor(private overlay: Overlay, private injector: Injector) {}

  openPopup(component: Type<any>, origin: HTMLElement) {
    this.closePopup();

    const positionStrategy = this.overlay.position()
      .flexibleConnectedTo(origin)
      .withPositions([
        { originX: 'end', originY: 'top', overlayX: 'start', overlayY: 'top' },
        { originX: 'start', originY: 'top', overlayX: 'end', overlayY: 'top' },
        { originX: 'end', originY: 'bottom', overlayX: 'start', overlayY: 'bottom' },
        { originX: 'start', originY: 'bottom', overlayX: 'end', overlayY: 'bottom' }
      ])
      .withPush(true);

    const scrollStrategy = this.overlay.scrollStrategies.reposition();

    this.currentOverlayRef = this.overlay.create({ 
      positionStrategy,
      scrollStrategy,
      hasBackdrop: true,
      backdropClass: 'transparent-backdrop',
      panelClass: 'popup-panel'
    });

    const portal = new ComponentPortal(component, null, this.injector);
    const componentRef = this.currentOverlayRef?.attach(portal);

    this.currentOverlayRef.backdropClick().subscribe(() => {
      this.closePopup();
    });

    this.currentOverlayRef?.keydownEvents().subscribe((event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        this.closePopup();
      }
    })

    return componentRef;
  }

  closePopup() {
    if (this.currentOverlayRef) {
      this.currentOverlayRef.dispose();
      this.currentOverlayRef = null;
      this.popupClosedSubject.next();
    }
  }
}

@Injectable({ providedIn: 'root' })
export class SearchCriteriaService {
  private criteria = {
    cities: [] as string[],
    dates: { start: null as Date | null, end: null as Date | null },
    weekdays: [] as string[],
    events: [] as string[],
    quantity: null as number | null
  };

  setCities(cities: string[]) {
    this.criteria.cities = cities;
    console.log('Search criteria updated - cities:', cities);
  }

  setDates(start: Date | null, end: Date | null) {
    this.criteria.dates = { start, end };
    console.log('Search criteria updated - dates:', { start, end });
  }

  setWeekdays(weekdays: string[]) {
    this.criteria.weekdays = weekdays;
    console.log('Search criteria updated - weekdays:', weekdays);
  }

  setEvents(events: string[]) {
    this.criteria.events = events;
    console.log('Search criteria updated - events:', events);
  }

  setQuantity(quantity: number | null) {
    this.criteria.quantity = quantity;
    console.log('Search criteria updated - quantity:', quantity);
  }

  getCriteria() {
    return { ...this.criteria };
  }

  clearCriteria() {
    this.criteria = {
      cities: [],
      dates: { start: null, end: null },
      weekdays: [],
      events: [],
      quantity: null
    };
  }

  sendRequest() {
    console.log('Sending requestusing data...', this.criteria)
  }
}
