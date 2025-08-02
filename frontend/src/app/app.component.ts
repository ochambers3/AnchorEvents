import { Component, OnInit, signal } from '@angular/core';
import { HomeComponent } from './features/home/home.component';
import { HousingLocationComponent } from './features/housing-location/housing-location.component';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from './layout/header/header.component';
import { FooterComponent } from './layout/footer/footer.component';

@Component({
  selector: 'app-root',
  imports: [HomeComponent, RouterModule, HeaderComponent, FooterComponent],
  // <img class="brand-logo" src="/assets/logo.svg" alt="logo" aria-hidden="true" />
  template: `
    <main>
      <app-header></app-header>
      <section class="content">
        <router-outlet></router-outlet>
      </section>
      <app-footer [class.hidden]="!showFooter()"></app-footer>
    </main>
  `,
  styleUrls: ['./app.component.css', './layout/header/header.component.css'],
  standalone: true
})
export class AppComponent implements OnInit {
  showFooter = signal(true);
  private lastScrollTop = 0;
  private scrollThreshold = 5;

  ngOnInit(): void {
    window.addEventListener('scroll', this.handleScroll, { passive: true });
  }

  // cleanup
  ngOnDestroy(): void {
    window.removeEventListener('scroll', this.handleScroll);
  }

  handleScroll = (): void => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollDiff = Math.abs(scrollTop - this.lastScrollTop);

    // Only trigger if scroll difference is above threshold
    if (scrollDiff < this.scrollThreshold) {
      return;
    }

    if (scrollTop > this.lastScrollTop && scrollTop > 100) {
      // Scrolling down and not at top
      this.showFooter.set(false);
    } else if (scrollTop < this.lastScrollTop) {
      // Scrolling up
      this.showFooter.set(true);
    }

    this.lastScrollTop = scrollTop;
  };

  
  title = 'Anchor Events';
}
