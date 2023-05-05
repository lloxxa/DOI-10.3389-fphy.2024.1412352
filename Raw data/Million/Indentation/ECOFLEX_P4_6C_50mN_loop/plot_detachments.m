% pillar number 6C

figure()
hold on
nfiles=227;
cmap=colormap(parula);
integrals= 1:nfiles;
peakstrain=1:nfiles;
for i=1:nfiles
    
    a=importdata(strcat("cup_",int2str(i),"_ret.csv"));
    z=a.data(:,3);
    b=baseline(a.data(:,5), 20);
    f=a.data(:,5)-b;
    
    z_0=z (  find(abs(f(1:500))==min(abs(f(1:500))))  );
    z_0=z_0(1);
    z=z-z_0;
    

    
    
    plot(z, f,'DisplayName', int2str(i), ...
        'Color', colorn(i, nfiles, cmap));
    xlabel('Strain (mm)', 'FontSize', 14);
    ylabel('Force (mN)', 'FontSize', 14);
    title('Repeated suction cup measurements', 'FontSize', 14);
    integrals(i)=-integrate(z,f);
    
    % get the baseline
    % find z-value of intersection = point of contact
    % integrate all f < baseline
    grad=gradient(f);
    maxgrad_idx=find(grad==max(grad));
    peakstrain(i)=z(maxgrad_idx(1));
    
end

colorbar();
caxis([1 nfiles]);

f=figure();
histogram(integrals, 40);
savefig(f);
xlim([0, 70]);
xlabel('Integral (mN/mm)', 'FontSize', 14);
ylabel('Bin Count', 'FontSize', 14);
title('Histogram of Integrals', 'FontSize', 14);


g=figure();
histogram(peakstrain, 40);
xlim([0, 1.8]);
xlabel('Peakstrain (mm)', 'FontSize', 14);
ylabel('Bin Count', 'FontSize', 14);
title('Histogram of Peakstrain', 'FontSize', 14);
savefig(g);

function sum_f=integrate(z,f)
    dz=z(end)/length(f(find(z==0):end));
    sum_f = sum( f(find(z==0):end) ) * dz;
end

function b=baseline(f, ntail)
    b=mean( f( length(f)-ntail:length(f)  ) );
end

% let's go functions
function c=colorn(i, ncolors, cmap)
    n=floor(256/ncolors*i);
    c=cmap(n,:);
end

